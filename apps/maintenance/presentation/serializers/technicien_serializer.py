"""
Serializers pour les techniciens (maintenance).
"""
from rest_framework import serializers

class TechnicienSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, required=False)  # lecture seule, non requis
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    cout_horaire = serializers.DecimalField(max_digits=8, decimal_places=2)

    def create(self, validated_data):
        # La création est gérée par le repository directement
        pass

    def update(self, instance, validated_data):
        # La mise à jour est gérée par le repository directement
        pass