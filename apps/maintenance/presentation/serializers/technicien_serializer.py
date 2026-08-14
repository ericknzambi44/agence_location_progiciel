"""
Sérialiseur pour les techniciens de maintenance.
"""

from rest_framework import serializers


class TechnicienSerializer(serializers.Serializer):
    """
    Sérialiseur pour les objets Technicien.
    """

    id = serializers.UUIDField(read_only=True, required=False)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    cout_horaire = serializers.DecimalField(max_digits=8, decimal_places=2)