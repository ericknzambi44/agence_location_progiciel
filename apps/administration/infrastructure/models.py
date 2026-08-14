#administration/infrastructure/models.py
from django.db import models
import uuid

class AgenceModel(models.Model):
    """
    Représente une agence (entité administrative).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200, unique=True)
    adresse_ligne1 = models.CharField(max_length=255)
    adresse_ligne2 = models.CharField(max_length=255, blank=True, null=True)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default='RDC')
    telephone = models.CharField(max_length=30)
    email = models.EmailField()
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_agence'


class ModuleConfigModel(models.Model):
    """
    Configuration des modules métier (Stock, RH, Maintenance, etc.).
    Chaque module peut être activé/désactivé par agence.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=30, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    ordre_affichage = models.IntegerField(default=0)
    parametres = models.JSONField(default=dict)

    # Champ pour lier la configuration à une agence (multi‑agences)
    agence_id = models.UUIDField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'admin_module_config'