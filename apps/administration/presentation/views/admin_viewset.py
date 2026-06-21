"""
ViewSet pour l'administration : agences et modules.
Tous les endpoints sont protégés par JWT.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID

from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository
# IMPORT CORRIGÉ : le fichier s'appelle django_module_config_repository
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


class AdminViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion administrative.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Désactiver la pagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agence_repo = DjangoAgenceRepository()
        self.module_repo = DjangoModuleConfigRepository()

    # --- LIST : GET /admin/ ---
    def list(self, request):
        """Retourne la liste des agences actives."""
        agences = self.agence_repo.list_actives()
        serializer = AgenceOutputSerializer(agences, many=True)
        return Response(serializer.data)

    # --- CREATE : POST /admin/ ---
    def create(self, request):
        """Crée une nouvelle agence."""
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

    # --- RETRIEVE : GET /admin/{id}/ ---
    def retrieve(self, request, pk=None):
     agence = self.agence_repo.get(UUID(pk))
     if not agence:
        return Response({"error": "Agence non trouvée"}, status=status.HTTP_404_NOT_FOUND)
     serializer = AgenceOutputSerializer(agence)
     return Response(serializer.data)

    # --- UPDATE : PUT /admin/{id}/ ---
    def update(self, request, pk=None):
        """Mise à jour complète d'une agence."""
        # À implémenter si nécessaire
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    # --- PARTIAL UPDATE : PATCH /admin/{id}/ ---
    def partial_update(self, request, pk=None):
        """Mise à jour partielle d'une agence."""
        # À implémenter si nécessaire
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    # --- DESTROY : DELETE /admin/{id}/ ---
    def destroy(self, request, pk=None):
        """Supprime une agence."""
        # À implémenter si nécessaire
        return Response({"error": "Non implémenté"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    # --------------------------------------------------------------
    #  MODULES
    # --------------------------------------------------------------

    @action(detail=False, methods=['get'], url_path='modules')
    def lister_modules(self, request):
        """GET /admin/modules/ → tous les modules."""
        modules = self.module_repo.list_all()
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='modules/actifs')
    def lister_modules_actifs(self, request):
        """GET /admin/modules/actifs/ → modules actifs."""
        use_case = ListerModulesActifsUseCase(self.module_repo)
        modules = use_case.execute()
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activer')
    def activer_module(self, request, pk=None):
        """POST /admin/modules/{id}/activer/ → active un module."""
        use_case = ActiverModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk))
            return Response({"status": "module activé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='desactiver')
    def desactiver_module(self, request, pk=None):
        """POST /admin/modules/{id}/desactiver/ → désactive un module."""
        use_case = DesactiverModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk))
            return Response({"status": "module désactivé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], url_path='configurer')
    def configurer_module(self, request, pk=None):
        """PATCH /admin/modules/{id}/configurer/ → met à jour les paramètres."""
        serializer = ModuleConfigParamInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        use_case = ConfigurerModuleUseCase(self.module_repo)
        try:
            use_case.execute(UUID(pk), serializer.validated_data['parametres'])
            return Response({"status": "configuration mise à jour"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)