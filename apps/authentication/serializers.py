"""
Serializers personnalisés pour le module d'authentification.
Gère l'enrichissement du payload JWT avec le RBAC, le contexte agence,
et l'exposition du profil utilisateur.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rh.infrastructure.models import EmployeModel

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer JWT personnalisé injectant le profil utilisateur,
    ses rôles (groupes), ses permissions et son agence dans le token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ------------------------------------------------------------------
        # 1. Informations de base de l'utilisateur
        # ------------------------------------------------------------------
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser

        # ------------------------------------------------------------------
        # 2. RBAC (Roles & Permissions)
        # ------------------------------------------------------------------
        roles = list(user.groups.values_list('name', flat=True))
        token['roles'] = roles

        permissions = list(user.get_all_permissions())
        token['permissions'] = permissions

        # ------------------------------------------------------------------
        # 3. Métier : Isolation Multi-Agence
        # ------------------------------------------------------------------
        agence_id = None
        if not user.is_superuser:
            try:
                employe = EmployeModel.objects.get(email=user.email)
                agence_id = employe.agence_id
            except EmployeModel.DoesNotExist:
                agence_id = None

        token['agence_id'] = agence_id

        return token


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'endpoint GET /auth/me/
    Expose le profil de l'utilisateur connecté avec son agence et le RBAC.
    """
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    agence_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_superuser',
            'roles',
            'permissions',
            'agence_id',
        ]

    def get_roles(self, obj) -> list[str]:
        return list(obj.groups.values_list('name', flat=True))

    def get_permissions(self, obj) -> list[str]:
        return list(obj.get_all_permissions())

    def get_agence_id(self, obj):
        if not obj.is_superuser:
            try:
                employe = EmployeModel.objects.get(email=obj.email)
                return employe.agence_id
            except EmployeModel.DoesNotExist:
                return None
        return None