"""
Sérialiseur pour les pièces détachées (module Maintenance).

Utilisé par l'API REST pour la validation et la sérialisation des objets PieceDetachee.
"""

from rest_framework import serializers


class PieceDetacheeSerializer(serializers.Serializer):
    """
    Sérialiseur pour les objets PieceDetachee.

    Champs :
        - id (UUID, read-only)        : identifiant unique de la pièce
        - reference (str)             : référence unique
        - nom (str)                   : nom de la pièce
        - prix_unitaire (Decimal)     : prix unitaire
        - stock (int)                 : quantité en stock
    """

    id = serializers.UUIDField(read_only=True)
    reference = serializers.CharField(max_length=50)
    nom = serializers.CharField(max_length=200)
    prix_unitaire = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock = serializers.IntegerField()