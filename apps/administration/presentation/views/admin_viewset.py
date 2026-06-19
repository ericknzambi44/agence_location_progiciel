from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID
from administration.infrastructure.repositories.django_module_repository import DjangoModuleConfigRepository
from administration.presentation.serializers.admin_serializers import (
    AgenceInputSerializer, AgenceOutputSerializer,
    ModuleConfigOutputSerializer, ModuleConfigParamInputSerializer
)
from administration.application.use_cases.creer_agence import CreerAgenceUseCase
from administration.application.use_cases.activer_module import ActiverModuleUseCase
from administration.application.use_cases.desactiver_module import DesactiverModuleUseCase
from administration.application.use_cases.configurer_module import ConfigurerModuleUseCase
from administration.application.use_cases.lister_modules_actifs import ListerModulesActifsUseCase
from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository

class AdminViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    # Désactiver la pagination pour ce ViewSet (retourne une liste brute)
    pagination_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agence_repo = DjangoAgenceRepository()
        self.module_repo = DjangoModuleConfigRepository()

    # --- LIST : GET /admin/ -> liste des agences actives ---
    def list(self, request):
        agences = self.agence_repo.list_actives()
        serializer = AgenceOutputSerializer(agences, many=True)
        return Response(serializer.data)

    # --- CREATE : POST /admin/ -> créer une agence ---
    def create(self, request):
        serializer = AgenceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uc = CreerAgenceUseCase(self.agence_repo)
        try:
            agence = uc.execute(
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

    # --- MODULES ---

    @action(detail=False, methods=['get'], url_path='modules', url_name='modules')
    def lister_modules(self, request):
        modules = self.module_repo.list_all()
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='modules/actifs', url_name='modules_actifs')
    def lister_modules_actifs(self, request):
        uc = ListerModulesActifsUseCase(self.module_repo)
        modules = uc.execute()
        serializer = ModuleConfigOutputSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activer', url_name='activer_module')
    def activer_module(self, request, pk=None):
        uc = ActiverModuleUseCase(self.module_repo)
        try:
            uc.execute(UUID(pk))
            return Response({"status": "module activé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=404)

    @action(detail=True, methods=['post'], url_path='desactiver', url_name='desactiver_module')
    def desactiver_module(self, request, pk=None):
        uc = DesactiverModuleUseCase(self.module_repo)
        try:
            uc.execute(UUID(pk))
            return Response({"status": "module désactivé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=404)

    @action(detail=True, methods=['patch'], url_path='configurer', url_name='configurer_module')
    def configurer_module(self, request, pk=None):
        serializer = ModuleConfigParamInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uc = ConfigurerModuleUseCase(self.module_repo)
        try:
            uc.execute(UUID(pk), serializer.validated_data['parametres'])
            return Response({"status": "configuration mise à jour"})
        except ValueError as e:
            return Response({"error": str(e)}, status=404)