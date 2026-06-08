from django.db import models
import uuid

class EmployeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matricule = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_embauche = models.DateField()
    taux_horaire = models.DecimalField(max_digits=8, decimal_places=2)
    poste = models.CharField(max_length=100)
    est_actif = models.BooleanField(default=True)
    role_id = models.UUIDField(null=True, blank=True)  # lien vers RoleModel

    class Meta:
        db_table = 'rh_employe'

class PointageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employe = models.ForeignKey(EmployeModel, on_delete=models.CASCADE)
    horodatage = models.DateTimeField()
    type = models.CharField(max_length=5, choices=[('ENTRY','Entrée'),('EXIT','Sortie')])
    commentaire = models.TextField(blank=True)

    class Meta:
        db_table = 'rh_pointage'

class EvaluationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employe = models.ForeignKey(EmployeModel, on_delete=models.CASCADE)
    date_evaluation = models.DateField()
    note = models.DecimalField(max_digits=3, decimal_places=1)  # 0.0 à 10.0
    commentaires = models.TextField(blank=True)
    evaluateur_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'rh_evaluation'

class RoleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50, unique=True)
    permissions = models.JSONField(default=list)  # stocke liste de codes

    class Meta:
        db_table = 'rh_role'