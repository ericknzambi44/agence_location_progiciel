from rest_framework import serializers

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
  
    montant_total = serializers.DecimalField(  
        max_digits=12,
        decimal_places=2,
        source='montant_total.valeur'
    )
    statut = serializers.CharField()