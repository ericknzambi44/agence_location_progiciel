"""
Modèles Django pour le module Maintenance.
Définissent les tables : techniciens, pièces détachées, interventions et leurs relations.
"""
from django.db import models
import uuid

class TechnicienModel(models.Model):
    """
    Représente un technicien de maintenance.
    Contient ses coordonnées et son coût horaire.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cout_horaire = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'maintenance_technicien'


class PieceDetacheeModel(models.Model):
    """
    Représente une pièce détachée (article de réparation) avec son stock.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True)  # Référence unique de la pièce
    nom = models.CharField(max_length=200)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'maintenance_piece'


class InterventionModel(models.Model):
    """
    Représente une intervention de maintenance sur un bien.
    Statut possible : planifiée, en cours, terminée, annulée.
    """
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien_id = models.UUIDField()  # Référence au bien du module Stock (pas de FK directe pour découplage)
    technicien = models.ForeignKey(TechnicienModel, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    cout_main_oeuvre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cout_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'maintenance_intervention'


class InterventionPieceModel(models.Model):
    """
    Table de liaison entre une intervention et les pièces utilisées, avec la quantité.
    Chaque paire (intervention, piece) est unique.
    """
    intervention = models.ForeignKey(
        InterventionModel,
        on_delete=models.CASCADE,
        related_name='pieces'  # Permet d'accéder aux pièces via intervention.pieces.all()
    )
    piece = models.ForeignKey(PieceDetacheeModel, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        db_table = 'maintenance_intervention_piece'
        unique_together = ('intervention', 'piece')