from rest_framework import serializers

class AgenceInputSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=200)
    adresse_ligne1 = serializers.CharField(max_length=255)
    adresse_ligne2 = serializers.CharField(required=False, allow_blank=True)
    code_postal = serializers.CharField(max_length=20)
    ville = serializers.CharField(max_length=100)
    pays = serializers.CharField(max_length=100, default='France')
    telephone = serializers.CharField(max_length=30)
    email = serializers.EmailField()

class AgenceOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    code = serializers.CharField()
    nom = serializers.CharField()
    adresse_ligne1 = serializers.CharField(source='adresse.rue')
    adresse_ligne2 = serializers.CharField(source='adresse.rue2', default='')  # si pas d'attribut rue2, ajustez
    code_postal = serializers.CharField(source='adresse.code_postal')
    ville = serializers.CharField(source='adresse.ville')
    pays = serializers.CharField(source='adresse.pays')
    telephone = serializers.CharField(source='telephone.value')
    email = serializers.EmailField(source='email.value')
    actif = serializers.BooleanField()
    date_creation = serializers.DateTimeField()

class ModuleConfigOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    code = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    ordre_affichage = serializers.IntegerField()
    parametres = serializers.JSONField()

class ModuleConfigParamInputSerializer(serializers.Serializer):
    parametres = serializers.JSONField()