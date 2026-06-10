# maintenance/infrastructure/models.py
from django.db import models
import uuid

class TechnicienModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cout_horaire = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'maintenance_technicien'


class PieceDetacheeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'maintenance_piece'


class InterventionModel(models.Model):
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien_id = models.UUIDField()  # référence au bien du module stock
    technicien = models.ForeignKey(TechnicienModel, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    cout_main_oeuvre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cout_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'maintenance_intervention'


class InterventionPieceModel(models.Model):
    intervention = models.ForeignKey(
        InterventionModel,
        on_delete=models.CASCADE,
        related_name='pieces'   # essentiel pour intervention.pieces.all() dans le mapper
    )
    piece = models.ForeignKey(PieceDetacheeModel, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        db_table = 'maintenance_intervention_piece'
        unique_together = ('intervention', 'piece')