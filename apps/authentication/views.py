"""
Vues REST pour le module d'authentification et RBAC.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from authentication.serializers import (
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Endpoint pour l'inscription d'un nouvel utilisateur.
    """
    # Implémentez la logique de création d'utilisateur ici
    return Response(
        {"message": "Inscription réussie. Vérifiez vos emails pour activer votre compte."},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    """
    Endpoint de validation du compte via le lien envoyé par email.
    """
    # Implémentez la vérification du jeton d'activation ici
    return Response(
        {"message": "Compte activé avec succès !"},
        status=status.HTTP_200_OK,
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue de connexion JWT personnalisée injectant le RBAC et l'agence_id.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    """
    Endpoint retournant les informations du profil connecté (GET /api/auth/me/).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)