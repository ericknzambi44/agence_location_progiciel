from rest_framework import serializers

class TechnicienSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    email = serializers.EmailField()
    cout_horaire = serializers.DecimalField(max_digits=8, decimal_places=2)