"""
Serializer pour la vérification de disponibilité des biens.
Réutilise le BienOutputSerializer pour la réponse.
"""
from rest_framework import serializers
from .bien_serializer import BienOutputSerializer


class DisponibiliteInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour les paramètres de vérification de disponibilité.
    """
    debut = serializers.DateField()
    fin = serializers.DateField()


class DisponibiliteOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la réponse de disponibilité.
    Retourne une liste de biens disponibles avec leurs détails.
    """
    biens = BienOutputSerializer(many=True)

    @staticmethod
    def from_biens(biens):
        return {'biens': [BienOutputSerializer.from_entity(b) for b in biens]}