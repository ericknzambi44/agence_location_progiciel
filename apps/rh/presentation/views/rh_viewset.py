"""
Module de Présentation - Ressources Humaines (Clean Architecture / DDD)

Expose les endpoints REST pour la gestion des employés, le suivi des pointages
et la récupération du profil de l'utilisateur connecté.
Applique les contrôles RBAC (HasModulePermission) et l'isolation multi-agence
via AgenceMixin.

Endpoints :
    GET    /api/rh/employes/                          -> Liste des employés
    POST   /api/rh/employes/                          -> Création d'un employé
    GET    /api/rh/employes/{uuid}/                   -> Détail d'un employé
    PUT    /api/rh/employes/{uuid}/                   -> Mise à jour d'un employé
    DELETE /api/rh/employes/{uuid}/                   -> Désactivation d'un employé
    GET    /api/rh/employes/actifs/                   -> Liste des employés actifs
    POST   /api/rh/pointages/                         -> Enregistrer un pointage
    GET    /api/rh/employes/{uuid}/pointages/YYYY-MM-DD/ -> Consultation des pointages
    GET    /api/rh/me/                                -> Profil de l'utilisateur connecté
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from rh.application.consulter_pointages import ConsulterPointagesUseCase
from rh.application.embaucher_employe import EmbaucherEmployeUseCase
from rh.application.enregistrer_pointage import EnregistrerPointageUseCase
from rh.infrastructure.models import Employe, Pointage
from rh.infrastructure.mappers.employe_mapper import EmployeMapper  # ✅ Ajout
from rh.infrastructure.repositories.django_employe_repository import DjangoEmployeRepository
from rh.infrastructure.repositories.django_pointage_repository import DjangoPointageRepository
from rh.presentation.serializers.rh_serializers import (
    EmployeInputSerializer,
    EmployeOutputSerializer,
    PointageInputSerializer,
    PointageOutputSerializer,
    MeSerializer,
)


class RHViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet principal du module Ressources Humaines.

    Regroupe les opérations CRUD sur les employés et les pointages,
    ainsi que la consultation du profil de l'utilisateur connecté.
    Toutes les actions sont protégées par le RBAC (module RH) et
    limitées aux données de l'agence de l'utilisateur.

    Attributs :
        permission_classes : Vérifie que l'utilisateur a accès au module RH.
        required_module    : Identifiant du module pour le contrôle d'accès.
    """

    permission_classes = [HasModulePermission]
    required_module = 'rh'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection des repositories concrets (infrastructure)
        self.employe_repo = DjangoEmployeRepository()
        self.pointage_repo = DjangoPointageRepository()

    # --------------------------------------------------------------------------
    # Surcharge de get_permissions pour définir required_model avant la vérification
    # --------------------------------------------------------------------------
    def get_permissions(self):
        """
        Définit dynamiquement le modèle requis en fonction de l'action courante,
        avant que la permission ne soit vérifiée par HasModulePermission.

        Cette approche garantit que `self.required_model` est toujours renseigné
        lorsque `has_permission` est appelé, évitant ainsi les erreurs 403
        dues à un modèle absent.
        """
        # Mapping action -> nom du modèle Django (pour les permissions)
        action_model_map = {
            'list': 'employe',
            'create': 'employe',
            'retrieve': 'employe',
            'update': 'employe',
            'destroy': 'employe',
            'lister_actifs': 'employe',
            'enregistrer_pointage': 'pointage',
            'consulter_pointages': 'pointage',
        }
        # L'action 'me' n'a pas besoin de modèle, elle utilise IsAuthenticated
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        # Pour 'me', on laisse permission_classes = [IsAuthenticated] déjà défini
        return super().get_permissions()

    # ==========================================================================
    # Gestion des employés
    # ==========================================================================

    def list(self, request):
        """
        GET /api/rh/employes/
        Liste l'ensemble des employés (actifs et inactifs) de l'agence.

        Permission requise : rh.view_employe
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        employes = self.employe_repo.list_all(agence_id=agence_id)
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST /api/rh/employes/
        Embaucher un nouvel employé et l'affecter à l'agence de l'utilisateur.

        Permission requise : rh.add_employe
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EmployeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        use_case = EmbaucherEmployeUseCase(self.employe_repo)
        try:
            employe = use_case.execute(
                matricule_str=data['matricule'],
                nom=data['nom'],
                prenom=data['prenom'],
                email_str=data['email'],
                date_embauche=data['date_embauche'],
                taux_valeur=data['taux_horaire'],
                poste=data['poste'],
                agence_id=agence_id,
            )
            output = EmployeOutputSerializer(employe).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        GET /api/rh/employes/{uuid}/
        Récupère un employé spécifique de l'agence.

        Permission requise : rh.view_employe
        """
        agence_id = self.get_agence_id()

        try:
            employe_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'employé invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employe = self.employe_repo.get(employe_uuid, agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeOutputSerializer(employe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        PUT /api/rh/employes/{uuid}/
        Met à jour un employé existant de l'agence.

        Permission requise : rh.change_employe
        """
        agence_id = self.get_agence_id()

        try:
            employe_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'employé invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employe = self.employe_repo.get(employe_uuid, agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Mise à jour des champs modifiables uniquement
        allowed_fields = [
            'nom', 'prenom', 'email', 'date_embauche',
            'taux_horaire', 'poste', 'est_actif'
        ]
        for field in allowed_fields:
            if field in data:
                setattr(employe, field, data[field])

        self.employe_repo.save(employe)
        output = EmployeOutputSerializer(employe).data
        return Response(output, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        DELETE /api/rh/employes/{uuid}/
        Désactive un employé (soft delete, ne supprime pas physiquement).

        Permission requise : rh.delete_employe
        """
        agence_id = self.get_agence_id()

        try:
            employe_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'employé invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employe = self.employe_repo.get(employe_uuid, agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Soft delete : on désactive l'employé (la désactivation de l'utilisateur
        # lié est gérée dans le repository si nécessaire)
        employe.desactiver()
        self.employe_repo.save(employe)

        return Response(
            {"message": "Employé désactivé avec succès."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='actifs')
    def lister_actifs(self, request):
        """
        GET /api/rh/employes/actifs/
        Retourne uniquement les employés actuellement actifs.

        Permission requise : rh.view_employe
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        employes = self.employe_repo.list_actifs(agence_id=agence_id)
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ==========================================================================
    # Pointages
    # ==========================================================================

    @action(detail=False, methods=['post'], url_path='pointages')
    def enregistrer_pointage(self, request):
        """
        POST /api/rh/pointages/
        Enregistre un pointage d'entrée ou de sortie pour un employé
        appartenant à la même agence que l'utilisateur connecté.

        Permission requise : rh.add_pointage
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PointageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Vérification que l'employé existe et appartient à l'agence
        employe = self.employe_repo.get(data['employe_id'], agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        use_case = EnregistrerPointageUseCase(self.employe_repo, self.pointage_repo)
        try:
            pointage = use_case.execute(
                employe_id=data['employe_id'],
                type_str=data['type'],
                horodatage=data.get('horodatage'),
            )
            output = PointageOutputSerializer(pointage).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='pointages/(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})')
    def consulter_pointages(self, request, pk=None, date_str=None):
        """
        GET /api/rh/employes/{employe_uuid}/pointages/YYYY-MM-DD/
        Retourne l'historique des pointages d'un employé pour une journée donnée.

        Permission requise : rh.view_pointage
        """
        agence_id = self.get_agence_id()

        try:
            employe_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'employé invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employe = self.employe_repo.get(employe_uuid, agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            jour = date.fromisoformat(date_str)
        except ValueError:
            return Response(
                {"error": "Format de date invalide (Format attendu : YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = ConsulterPointagesUseCase(self.pointage_repo, self.employe_repo)
        try:
            pointages = use_case.execute(employe_uuid, jour)
            serializer = PointageOutputSerializer(pointages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # ==========================================================================
    # Profil de l'utilisateur connecté
    # ==========================================================================

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        GET /api/rh/me/
        Retourne le profil complet de l'employé connecté, ses informations
        d'agence et la liste de ses permissions RBAC (déduites des groupes).

        Accessible à tout utilisateur authentifié (pas de permission
        spécifique de module requise).
        """
        user = request.user

        try:
            employe_model = user.employe_rh
        except Employe.DoesNotExist:
            return Response(
                {"error": "Aucun employé associé à cet utilisateur."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Convertir le modèle Django en entité domaine pour le sérialiseur
        employe_domain = EmployeMapper.to_domain(employe_model)
        permissions = list(user.get_all_permissions())

        serializer = MeSerializer({
            'employe': employe_domain,
            'permissions': permissions,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)