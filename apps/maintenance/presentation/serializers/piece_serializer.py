"""
Sérialiseur pour les pièces détachées.
Utilisé par l'API REST pour la validation et la sérialisation.
"""
from rest_framework import serializers


class PieceDetacheeSerializer(serializers.Serializer):
    """
    Sérialiseur pour les objets PieceDetachee.
    Tous les champs sont requis pour la création.
    """
    id = serializers.UUIDField(read_only=True)
    reference = serializers.CharField(max_length=50)
    nom = serializers.CharField(max_length=200)
    prix_unitaire = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock = serializers.IntegerField()