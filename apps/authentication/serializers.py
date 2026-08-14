"""
Sérialiseurs du module d'authentification.
"""

from rest_framework import serializers
from rh.infrastructure.models import Employe


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Sérialiseur personnalisé pour la connexion JWT.
    Ajoute des informations sur l'employé et ses rôles.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth.models import User
        from django.contrib.auth import authenticate
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")

        # Vérifier si un employé est lié
        try:
            employe = Employe.objects.get(user=user)
        except Employe.DoesNotExist:
            raise serializers.ValidationError("Aucun employé associé à cet utilisateur.")

        # Ajouter des informations au token
        token_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'employe_id': str(employe.id),
            'agence_id': str(employe.agence_id),
        }
        # On peut utiliser les méthodes de SimpleJWT pour générer le token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        refresh['employe_id'] = str(employe.id)
        refresh['agence_id'] = str(employe.agence_id)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs