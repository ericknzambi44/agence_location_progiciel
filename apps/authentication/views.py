"""
Vues du module d'authentification.

Gère l'enregistrement des utilisateurs, l'activation par email,
la connexion JWT, la consultation du profil utilisateur connecté,
et une vue d'administration pour synchroniser les permissions RBAC.
"""

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import CustomTokenObtainPairSerializer
from rh.infrastructure.models import Employe
from rh.infrastructure.mappers.employe_mapper import EmployeMapper
from rh.presentation.serializers.rh_serializers import MeSerializer

User = get_user_model()


# --------------------------------------------------------------------------
# Vue de connexion JWT personnalisée
# --------------------------------------------------------------------------

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Authentifie l'utilisateur et retourne un couple de tokens JWT
    (access + refresh) enrichi avec les rôles, permissions et agence.
    """
    serializer_class = CustomTokenObtainPairSerializer


# --------------------------------------------------------------------------
# Enregistrement d'un nouvel utilisateur
# --------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/auth/register/
    Crée un nouvel utilisateur inactif et envoie un email d'activation.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    if not username or not email or not password or not password_confirm:
        return Response(
            {"error": "Tous les champs sont obligatoires : username, email, password, password_confirm."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if password != password_confirm:
        return Response(
            {"error": "Les mots de passe ne correspondent pas."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Ce nom d'utilisateur est déjà pris."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Cette adresse email est déjà utilisée."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False
    )

    return Response(
        {
            "message": "Utilisateur créé avec succès. Veuillez vérifier votre email pour activer votre compte.",
            "user_id": user.pk,
            "username": user.username,
            "email": user.email,
        },
        status=status.HTTP_201_CREATED
    )


# --------------------------------------------------------------------------
# Activation du compte utilisateur par email
# --------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    """
    GET /api/auth/activate/<uidb64>/<token>/
    Active un compte utilisateur après validation du lien reçu par email.
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response(
            {"message": "Compte activé avec succès. Vous pouvez maintenant vous connecter."},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Le lien d'activation est invalide ou a expiré."},
            status=status.HTTP_400_BAD_REQUEST
        )


# --------------------------------------------------------------------------
# Profil de l'utilisateur connecté
# --------------------------------------------------------------------------

class UserProfileView(APIView):
    """
    GET /api/auth/me/
    Retourne le profil complet de l'utilisateur connecté, incluant
    ses informations d'employé, son agence et ses permissions RBAC.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            employe_model = user.employe_rh
        except Employe.DoesNotExist:
            return Response(
                {"error": "Aucun employé associé à cet utilisateur."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Convertir le modèle Django en entité domaine pour le sérialiseur
        employe_domain = EmployeMapper.to_domain(employe_model)
        permissions = list(user.get_all_permissions())

        serializer = MeSerializer({
            'employe': employe_domain,
            'permissions': permissions,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------------------------------------------------------
# Vue d'administration : synchronisation RBAC
# --------------------------------------------------------------------------

@staff_member_required
def sync_rbac_admin_view(request):
    """
    Vue admin pour synchroniser les permissions RBAC.
    Affiche un bouton et exécute la commande `sync_rbac` en POST.
    """
    context = {
        'title': 'Synchronisation RBAC',
        'opts': None,
    }

    if request.method == 'POST':
        try:
            call_command('sync_rbac', '--create-groups')
            messages.success(request, "RBAC synchronisé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la synchronisation : {e}")
        return redirect('sync_rbac')

    return render(request, 'admin/sync_rbac.html', context)