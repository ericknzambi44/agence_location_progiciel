from django.db import models
import uuid

class CategorieModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'stock_categorie'

class BienModel(models.Model):
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
    date_achat = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible')
    categorie = models.ForeignKey(CategorieModel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'stock_bien'

class MouvementStockModel(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('reservation', 'Réservation'),
        ('annulation_reservation', 'Annulation réservation'),
        ('retour', 'Retour'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien = models.ForeignKey(BienModel, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    type_mouvement = models.CharField(max_length=25, choices=TYPE_CHOICES)
    date_heure = models.DateTimeField(auto_now_add=True)
    reference_document = models.CharField(max_length=100, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'stock_mouvement'

class DisponibilitePeriodeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bien = models.ForeignKey(BienModel, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    est_reserve = models.BooleanField(default=False)
    reservation_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'stock_disponibilite'