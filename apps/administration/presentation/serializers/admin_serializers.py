"""
Serializers pour l'API d'administration.
Gèrent la validation et la sérialisation des agences et des modules.
"""
from rest_framework import serializers


class AgenceInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la création/modification d'une agence.
    Attend des champs plats (adresse_ligne1, adresse_ligne2, etc.).
    """
    nom = serializers.CharField(max_length=200)
    adresse_ligne1 = serializers.CharField(max_length=255)
    adresse_ligne2 = serializers.CharField(required=False, allow_blank=True, default="")
    code_postal = serializers.CharField(required=False, allow_blank=True, default="")
    ville = serializers.CharField(max_length=100)
    pays = serializers.CharField(max_length=100, default="RDC")
    telephone = serializers.CharField(max_length=30)
    email = serializers.EmailField()


class AgenceOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la réponse des agences.
    Extrait les champs depuis l'objet adresse de l'entité.
    """
    id = serializers.UUIDField()
    code = serializers.CharField()
    nom = serializers.CharField()
    actif = serializers.BooleanField()
    date_creation = serializers.DateTimeField()

    # Champs d'adresse extraits via SerializerMethodField
    adresse_ligne1 = serializers.SerializerMethodField()
    adresse_ligne2 = serializers.SerializerMethodField()
    code_postal = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    pays = serializers.SerializerMethodField()

    telephone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_adresse_ligne1(self, obj):
        return obj.adresse.ligne1 if obj.adresse else ""

    def get_adresse_ligne2(self, obj):
        return obj.adresse.ligne2 if obj.adresse else ""

    def get_code_postal(self, obj):
        return obj.adresse.code_postal if obj.adresse else ""

    def get_ville(self, obj):
        return obj.adresse.ville if obj.adresse else ""

    def get_pays(self, obj):
        return obj.adresse.pays if obj.adresse else ""

    def get_telephone(self, obj):
        return obj.telephone.value if obj.telephone else ""

    def get_email(self, obj):
        return obj.email.value if obj.email else ""


class ModuleConfigOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour les modules configurables.
    """
    id = serializers.UUIDField()
    code = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    ordre_affichage = serializers.IntegerField()
    parametres = serializers.JSONField()


class ModuleConfigParamInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la configuration des paramètres d'un module.
    """
    parametres = serializers.JSONField()