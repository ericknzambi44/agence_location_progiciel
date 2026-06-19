from rest_framework import serializers

class PieceDetacheeSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference = serializers.CharField()
    nom = serializers.CharField()
    prix_unitaire = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock = serializers.IntegerField()