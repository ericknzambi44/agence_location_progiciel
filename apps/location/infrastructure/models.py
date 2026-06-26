from django.db import models
import uuid
from location.domain.value_objects.regle_tarification import TypeRegle


class ClientModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=30)
    adresse = models.TextField()
    est_actif = models.BooleanField(default=True)

    class Meta:
        db_table = 'location_client'


class ContratModel(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(ClientModel, on_delete=models.PROTECT)
    bien_id = models.UUIDField()  # référence au bien (pas de FK directe)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')

    class Meta:
        db_table = 'location_contrat'


class RegleTarificationModel(models.Model):
    """
    Modèle Django pour les règles de tarification.
    Supporte le ciblage par bien, par catégorie, ou global.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agence_id = models.UUIDField(db_index=True)
    type = models.CharField(max_length=10, choices=[(t.value, t.value) for t in TypeRegle])
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    duree_min = models.PositiveIntegerField()
    duree_max = models.PositiveIntegerField(null=True, blank=True)

    # Ciblage : bien spécifique ou catégorie (ou global si les deux sont null)
    bien_id = models.UUIDField(null=True, blank=True, db_index=True)
    categorie_id = models.UUIDField(null=True, blank=True, db_index=True)

    periode_debut = models.DateField(null=True, blank=True)
    periode_fin = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'location_regle_tarification'
        # Contrainte pour garantir qu'une règle ne cible pas à la fois un bien et une catégorie
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