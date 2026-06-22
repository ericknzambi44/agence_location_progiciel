from rest_framework import serializers

from location.domain.value_objects.regle_tarification import TypeRegle


class ClientInputSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=30)
    adresse = serializers.CharField()


class ClientOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    email = serializers.EmailField()
    telephone = serializers.CharField()
    adresse = serializers.CharField()
    est_actif = serializers.BooleanField()


class ContratInputSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    date_debut = serializers.DateField()
    date_fin = serializers.DateField()


class ContratOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    client_id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    date_debut = serializers.DateField()
    date_fin = serializers.DateField()
    montant_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    statut = serializers.CharField()




class RegleTarificationSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[t.value for t in TypeRegle])
    valeur = serializers.DecimalField(max_digits=10, decimal_places=2)
    duree_min = serializers.IntegerField(min_value=0)
    duree_max = serializers.IntegerField(required=False, allow_null=True)
    type_bien_id = serializers.UUIDField(required=False, allow_null=True)
    periode_debut = serializers.DateField(required=False, allow_null=True)
    periode_fin = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)


class RegleTarificationInputSerializer(serializers.Serializer):
    regles = RegleTarificationSerializer(many=True)


class RegleTarificationOutputSerializer(RegleTarificationSerializer):
    pass    