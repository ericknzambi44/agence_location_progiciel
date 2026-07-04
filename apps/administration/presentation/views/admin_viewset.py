"""
ViewSet pour l'administration : agences et modules.
Tous les endpoints sont protégés par JWT.
Filtrage des modules par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from uuid import UUID

from config.mixins import AgenceMixin

from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository
from administration.infrastructure.repositories.django_module_config_repository import DjangoModuleConfigRepository
from administration.presentation.serializers.admin_serializers import (
    AgenceInputSerializer,
    AgenceOutputSerializer,
    ModuleConfigOutputSerializer,
    ModuleConfigParamInputSerializer,
)
from administration.application.use_cases.creer_agence import CreerAgenceUseCase
from administration.application.use_cases.activer_module import ActiverModuleUseCase
from administration.application.use_cases.desactiver_module import DesactiverModuleUseCase
from administration.application.use_cases.configurer_module import ConfigurerModuleUseCase
from administration.application.use_cases.lister_modules_actifs import ListerModulesActifsUseCase


class AdminViewSet(AgenceMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agence_repo = DjangoAgenceRepository()
        self.module_repo = DjangoModuleConfigRepository()

    def list(self, request):
        """
        Retourne la liste des agences accessibles à l'utilisateur.
        """
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        if request.user.is_superuser:
            agences = self.agence_repo.list_actives()
        else:
            agence = self.agence_repo.get(agence_id) if agence_id else None
            agences = [agence] if agence else []

        serializer = AgenceOutputSerializer(agences, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Crée une nouvelle agence.
        """
        serializer = AgenceInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        use_case = CreerAgenceUseCase(self.agence_repo)
        try:
            agence = use_case.execute(
                nom=data['nom'],
                adresse_ligne1=data['adresse_ligne1'],
                adresse_ligne2=data.get('adresse_ligne2', ''),
                code_postal=data['code_postal'],
                ville=data['ville'],
                pays=data['pays'],
                telephone=data['telephone'],
                email=data['email']
            )
            output = AgenceOutputSerializer(agence).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        agence = self.agence_repo.get(UUID(pk))
        if not agence:
            return Response({"error": "Agence non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AgenceOutputSerializer(agence)
        return Response(serializer.data)

    def update(self, request, pk=None):
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def partial_update(self, request, pk=None):
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, pk=None):
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(detail=False, methods=['get'], url_path='modules')
    def lister_modules(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        modules = self.module_repo.list_all(agence_id=agence_id)
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='modules/actifs')
    def lister_modules_actifs(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        use_case = ListerModulesActifsUseCase(self.module_repo)
        modules = use_case.execute(agence_id=agence_id)
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activer')
    def activer_module(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        module = self.module_repo.get(UUID(pk), agence_id=agence_id)
        if not module:
            return Response({"error": "Module non trouvé ou non autorisé"}, status=status.HTTP_404_NOT_FOUND)

        use_case = ActiverModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk), agence_id=agence_id)
            return Response({"status": "module activé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='desactiver')
    def desactiver_module(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        module = self.module_repo.get(UUID(pk), agence_id=agence_id)
        if not module:
            return Response({"error": "Module non trouvé ou non autorisé"}, status=status.HTTP_404_NOT_FOUND)

        use_case = DesactiverModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk), agence_id=agence_id)
            return Response({"status": "module désactivé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], url_path='configurer')
    def configurer_module(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        module = self.module_repo.get(UUID(pk), agence_id=agence_id)
        if not module:
            return Response({"error": "Module non trouvé ou non autorisé"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuleConfigParamInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        use_case = ConfigurerModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk), serializer.validated_data['parametres'], agence_id=agence_id)
            return Response({"status": "configuration mise à jour"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)