from rest_framework import serializers

class EmployeInputSerializer(serializers.Serializer):
    matricule = serializers.CharField(max_length=10)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    date_embauche = serializers.DateField()
    taux_horaire = serializers.DecimalField(max_digits=8, decimal_places=2)
    poste = serializers.CharField(max_length=100)

class EmployeOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    matricule = serializers.CharField(source='matricule.value')
    nom = serializers.CharField(source='nom.value')
    prenom = serializers.CharField(source='prenom.value')
    email = serializers.EmailField(source='email.value')
    date_embauche = serializers.DateField()
    taux_horaire = serializers.DecimalField(max_digits=8, decimal_places=2, source='taux_horaire.valeur')
    poste = serializers.CharField()
    est_actif = serializers.BooleanField()

class PointageInputSerializer(serializers.Serializer):
    employe_id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=['ENTRY', 'EXIT'])
    horodatage = serializers.DateTimeField(required=False)

class PointageOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    employe_id = serializers.UUIDField()
    horodatage = serializers.DateTimeField()
    type = serializers.CharField()