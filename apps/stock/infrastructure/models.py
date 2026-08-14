"""
Modèles de données du module Stock.

Ce module gère :
    - Les catégories de biens (Categorie)
    - Les biens (Bien)
    - Les mouvements de stock (MouvementStock)
    - Les périodes de disponibilité (DisponibilitePeriode)

Architecture :
    - Modèles Django (infrastructure) mappés vers les entités du domaine.
    - Clé primaire UUID pour un référencement stable.
    - Conventions de nommage sans suffixe "Model".
    - Champs agence en ForeignKey pour une isolation multi-agences robuste.
"""

from django.db import models
import uuid


class Categorie(models.Model):
    """
    Catégorie de biens (ex: véhicules, appareils électroniques, etc.).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='categories_stock',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'stock'
        db_table = 'stock_categorie'
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Bien(models.Model):
    """
    Bien stocké et louable (ex: voiture, machine, etc.).
    """

    ETAT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_maintenance', 'En maintenance'),
        ('endommage', 'Endommagé'),
        ('archive', 'Archivé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    prix_unitaire_ht = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    devise = models.CharField(max_length=3, default='USD')
    date_achat = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible')
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='biens_stock',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'stock'
        db_table = 'stock_bien'
        verbose_name = "Bien"
        verbose_name_plural = "Biens"
        ordering = ['reference']

    def __str__(self):
        return f"{self.reference} - {self.nom}"


class MouvementStock(models.Model):
    """
    Mouvement de stock (entrée, sortie, réservation, etc.).
    """

    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('reservation', 'Réservation'),
        ('annulation_reservation', 'Annulation réservation'),
        ('retour', 'Retour'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    type_mouvement = models.CharField(max_length=25, choices=TYPE_CHOICES)
    date_heure = models.DateTimeField(auto_now_add=True)
    reference_document = models.CharField(max_length=100, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'stock'
        db_table = 'stock_mouvement'
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_heure']

    def __str__(self):
        return f"{self.bien.reference} - {self.type_mouvement} ({self.quantite})"


class DisponibilitePeriode(models.Model):
    """
    Période de disponibilité ou de réservation d'un bien.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    est_reserve = models.BooleanField(default=False)
    reservation_id = models.UUIDField(null=True, blank=True)

    class Meta:
        app_label = 'stock'
        db_table = 'stock_disponibilite'
        verbose_name = "Période de disponibilité"
        verbose_name_plural = "Périodes de disponibilité"
        ordering = ['date_debut']

    def __str__(self):
        return f"{self.bien.reference} du {self.date_debut} au {self.date_fin}"