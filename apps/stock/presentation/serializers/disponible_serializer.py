"""
Sérialiseurs pour la vérification de disponibilité des biens.

Réutilise `BienOutputSerializer` pour la réponse.
"""

from rest_framework import serializers
from .bien_serializer import BienOutputSerializer


class DisponibiliteInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour les paramètres de vérification de disponibilité.

    Champs :
        - debut (date) : date de début de la période
        - fin (date)   : date de fin de la période
    """

    debut = serializers.DateField()
    fin = serializers.DateField()


class DisponibiliteOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie pour la réponse de disponibilité.

    Structure :
        {
            "biens": [ ... ]   # liste de biens disponibles
        }
    """

    biens = BienOutputSerializer(many=True)