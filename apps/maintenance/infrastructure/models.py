"""
Modèles de données du module Maintenance.

Gère :
    - Les techniciens (Technicien)
    - Les pièces détachées (PieceDetachee)
    - Les interventions (Intervention)
    - Les pièces utilisées par intervention (InterventionPiece)
    - Les règles de tarification (RegleMaintenance)

Architecture :
    - Noms de modèles sans suffixe "Model".
    - Clé primaire UUID.
    - Champs `agence` en ForeignKey vers `administration.AgenceModel`.
    - `app_label = 'maintenance'` pour l'enregistrement correct.
"""

from django.db import models
import uuid


class Technicien(models.Model):
    """
    Représente un technicien de maintenance.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    cout_horaire = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Coût horaire"
    )

    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='techniciens_maintenance',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'maintenance'
        db_table = 'maintenance_technicien'
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class PieceDetachee(models.Model):
    """
    Représente une pièce détachée avec son stock.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    prix_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Prix unitaire"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='pieces_maintenance',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'maintenance'
        db_table = 'maintenance_piece'
        verbose_name = "Pièce détachée"
        verbose_name_plural = "Pièces détachées"
        ordering = ['reference']

    def __str__(self):
        return f"{self.reference} - {self.nom}"


class Intervention(models.Model):
    """
    Représente une intervention de maintenance sur un bien.
    """

    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien_id = models.UUIDField(verbose_name="ID du bien (référence externe)")
    technicien = models.ForeignKey(
        Technicien,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Technicien"
    )
    date_debut = models.DateTimeField(verbose_name="Début")
    date_fin = models.DateTimeField(verbose_name="Fin")
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifiee',
        verbose_name="Statut"
    )
    cout_main_oeuvre = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Coût main d'œuvre"
    )
    cout_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Coût total"
    )

    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True,
        related_name='interventions_maintenance',
        verbose_name="Agence"
    )

    class Meta:
        app_label = 'maintenance'
        db_table = 'maintenance_intervention'
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"
        ordering = ['-date_debut']

    def __str__(self):
        return f"Intervention {self.id} - {self.statut}"


class InterventionPiece(models.Model):
    """
    Table de liaison entre une intervention et les pièces utilisées.
    """

    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name='pieces',
        verbose_name="Intervention"
    )
    piece = models.ForeignKey(
        PieceDetachee,
        on_delete=models.CASCADE,
        verbose_name="Pièce"
    )
    quantite = models.PositiveIntegerField(verbose_name="Quantité")

    class Meta:
        app_label = 'maintenance'
        db_table = 'maintenance_intervention_piece'
        unique_together = ('intervention', 'piece')
        verbose_name = "Pièce utilisée"
        verbose_name_plural = "Pièces utilisées"

    def __str__(self):
        return f"{self.piece.reference} x{self.quantite}"


class RegleMaintenance(models.Model):
    """
    Règle de tarification pour la maintenance.
    """

    TYPE_CHOICES = [
        ('forfait', 'Forfait'),
        ('remise', 'Remise'),
        ('majoration', 'Majoration'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agence = models.ForeignKey(
        'administration.AgenceModel',
        on_delete=models.PROTECT,
        db_index=True,
        related_name='regles_maintenance',
        verbose_name="Agence"
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Type")
    valeur = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur")
    duree_min = models.PositiveIntegerField(default=0, verbose_name="Durée min (h)")
    duree_max = models.PositiveIntegerField(null=True, blank=True, verbose_name="Durée max (h)")
    periode_debut = models.DateField(null=True, blank=True, verbose_name="Période début")
    periode_fin = models.DateField(null=True, blank=True, verbose_name="Période fin")
    description = models.TextField(blank=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        app_label = 'maintenance'
        db_table = 'maintenance_regle_tarification'
        verbose_name = "Règle de maintenance"
        verbose_name_plural = "Règles de maintenance"
        ordering = ['periode_debut']

    def __str__(self):
        return f"{self.get_type_display()} - {self.valeur}"