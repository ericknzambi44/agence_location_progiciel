"""
Modèles de données du module Location.

Gère :
    - Les clients (Client)
    - Les contrats de location (Contrat)
    - Les règles de tarification (RegleTarification)

Architecture :
    - Noms de modèles sans suffixe "Model".
    - Clé primaire UUID.
    - Isolation multi-agences via ForeignKey vers l'agence.
    - `app_label = 'location'` pour l'enregistrement correct.
"""

from django.db import models
import uuid

from location.domain.value_objects.regle_tarification import TypeRegle


class Client(models.Model):
    """
    Client d'une agence de location.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=30, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse")
    est_actif = models.BooleanField(default=True, verbose_name="Actif")

    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='clients_location',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'location'
        db_table = 'location_client'
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Contrat(models.Model):
    """
    Contrat de location liant un client, un bien et une période.
    """

    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Client"
    )
    bien_id = models.UUIDField(verbose_name="ID du bien (référence externe)")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant total"
    )
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='actif',
        verbose_name="Statut"
    )

    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='contrats_location',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'location'
        db_table = 'location_contrat'
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"
        ordering = ['-date_debut']

    def __str__(self):
        return f"Contrat {self.id} - {self.client}"


class RegleTarification(models.Model):
    """
    Règle de tarification pour les locations.

    Supporte le ciblage par bien, par catégorie, ou global.
    Liée à une agence.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        db_index=True,
        related_name='regles_location',
        verbose_name="Agence"
    )
    type = models.CharField(
        max_length=10,
        choices=[(t.value, t.value) for t in TypeRegle],
        verbose_name="Type"
    )
    valeur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valeur"
    )
    duree_min = models.PositiveIntegerField(verbose_name="Durée min")
    duree_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Durée max"
    )

    # Ciblage : bien spécifique ou catégorie (ou global si les deux sont null)
    bien_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="ID du bien cible"
    )
    categorie_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="ID de la catégorie cible"
    )

    periode_debut = models.DateField(null=True, blank=True, verbose_name="Période début")
    periode_fin = models.DateField(null=True, blank=True, verbose_name="Période fin")
    description = models.TextField(blank=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        app_label = 'location'
        db_table = 'location_regle_tarification'
        verbose_name = "Règle de tarification"
        verbose_name_plural = "Règles de tarification"
        ordering = ['periode_debut']
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(bien_id__isnull=True, categorie_id__isnull=True) |
                    models.Q(bien_id__isnull=False, categorie_id__isnull=True) |
                    models.Q(bien_id__isnull=True, categorie_id__isnull=False)
                ),
                name='either_bien_or_categorie'
            )
        ]

    def __str__(self):
        return f"{self.type} - {self.valeur}"