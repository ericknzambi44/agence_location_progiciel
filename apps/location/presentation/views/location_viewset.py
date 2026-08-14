"""
Module de Présentation - Location (Clean Architecture / DDD)

Expose les cas d'utilisation de la gestion des clients, des contrats et
des règles de tarification via des endpoints HTTP.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from location.application.services.tarification_service import TarificationService
from location.application.use_cases.calculer_montant import CalculerMontantLocationUseCase
from location.application.use_cases.consulter_contrats import ConsulterContratsUseCase
from location.application.use_cases.creer_client import CreerClientUseCase
from location.application.use_cases.louer_bien import LouerBienUseCase
from location.application.use_cases.retourner_bien import RetournerBienUseCase
from location.infrastructure.repositories.django_client_repository import DjangoClientRepository
from location.infrastructure.repositories.django_contrat_repository import DjangoContratRepository
from location.infrastructure.repositories.django_regle_tarification_repository import (
    DjangoRegleTarificationRepository,
)
from location.presentation.serializers.location_serializers import (
    ClientInputSerializer,
    ClientOutputSerializer,
    ContratInputSerializer,
    ContratOutputSerializer,
)
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository


class LocationViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant la relation client, la création de contrats et le processus de retour.

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'location'
        Le modèle requis est défini dynamiquement selon l'action.
    """

    permission_classes = [HasModulePermission]
    required_module = 'location'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection des repositories et services de domaine
        self.client_repo = DjangoClientRepository()
        self.contrat_repo = DjangoContratRepository()
        self.bien_repo = DjangoBienRepository()
        regle_repo = DjangoRegleTarificationRepository()
        self.tarif_service = TarificationService(regle_repo)

    # --------------------------------------------------------------------------
    # Mapping action -> modèle pour permissions RBAC
    # --------------------------------------------------------------------------
    def get_permissions(self):
        """
        Associe chaque action au nom de modèle Django attendu par la permission.
        Les noms sont sans suffixe `Model` (ex: 'client', 'contrat').
        """
        action_model_map = {
            'create_client': 'client',
            'list_clients': 'client',
            'create_contrat': 'contrat',
            'list_contrats': 'contrat',
            'retourner': 'contrat',
            'calculer_montant': 'contrat',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Gestion des clients
    # --------------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='clients/creer')
    def create_client(self, request):
        """
        POST /api/location/clients/creer/
        Enregistre un nouveau client rattaché à l'agence de l'utilisateur.

        Permission requise : location.add_client
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreerClientUseCase(self.client_repo)
        try:
            client = use_case.execute(**serializer.validated_data, agence_id=agence_id)
            output = ClientOutputSerializer(client).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='clients')
    def list_clients(self, request):
        """
        GET /api/location/clients/
        Consulte l'annuaire des clients de l'agence.

        Permission requise : location.view_client
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        clients = self.client_repo.list_all(agence_id=agence_id)
        serializer = ClientOutputSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --------------------------------------------------------------------------
    # Gestion des contrats
    # --------------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='contrats/creer')
    def create_contrat(self, request):
        """
        POST /api/location/contrats/creer/
        Génère un nouveau contrat de location.

        Permission requise : location.add_contrat
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ContratInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        use_case = LouerBienUseCase(
            self.contrat_repo,
            self.client_repo,
            self.bien_repo,
            self.tarif_service,
        )
        try:
            contrat = use_case.execute(
                client_id=data['client_id'],
                bien_id=data['bien_id'],
                agence_id=agence_id,
                date_debut=data['date_debut'],
                date_fin=data['date_fin'],
            )
            output = ContratOutputSerializer(contrat).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='contrats')
    def list_contrats(self, request):
        """
        GET /api/location/contrats/
        Consulte la liste complète des contrats de location de l'agence.

        Permission requise : location.view_contrat
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        use_case = ConsulterContratsUseCase(self.contrat_repo)
        contrats = use_case.execute(agence_id=agence_id)
        serializer = ContratOutputSerializer(contrats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='retourner')
    def retourner(self, request, pk=None):
        """
        POST /api/location/{contrat_uuid}/retourner/
        Clôture un contrat actif en marquant le bien comme retourné.

        Permission requise : location.change_contrat
        """
        agence_id = self.get_agence_id()
        try:
            contrat_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant de contrat UUID invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contrat = self.contrat_repo.get(contrat_uuid, agence_id=agence_id)
        if not contrat:
            return Response(
                {"error": "Contrat non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        use_case = RetournerBienUseCase(self.contrat_repo)
        try:
            use_case.execute(contrat_uuid)
            return Response(
                {"status": "success", "message": "Contrat terminé et bien réintégré."},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --------------------------------------------------------------------------
    # Calcul du montant estimé
    # --------------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='calculer-montant')
    def calculer_montant(self, request):
        """
        POST /api/location/calculer-montant/
        Simule et calcule le coût estimé d'une location.

        Permission requise : location.view_contrat
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        bien_id = request.data.get('bien_id')
        date_debut = request.data.get('date_debut')
        date_fin = request.data.get('date_fin')

        if not bien_id or not date_debut or not date_fin:
            return Response(
                {"error": "Les champs bien_id, date_debut et date_fin sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            debut = date.fromisoformat(date_debut)
            fin = date.fromisoformat(date_fin)
            uuid_bien = UUID(bien_id)
        except ValueError:
            return Response(
                {"error": "Format d'identifiant ou de date invalide (Format attendu : YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = CalculerMontantLocationUseCase(self.bien_repo, self.tarif_service)
        try:
            montant = use_case.execute(uuid_bien, agence_id, debut, fin)
            return Response(
                {"montant_total": float(montant.valeur)},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)