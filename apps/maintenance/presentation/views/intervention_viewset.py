"""
Module de Présentation - Maintenance (Clean Architecture / DDD)

Expose les cas d'utilisation de gestion des interventions, pièces détachées et techniciens.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from maintenance.application.services.tarification_maintenance_service import (
    TarificationMaintenanceService,
)
from maintenance.application.use_cases.ajouter_piece import AjouterPieceUseCase
from maintenance.application.use_cases.calculer_cout_intervention import CalculerCoutInterventionUseCase
from maintenance.application.use_cases.demarrer_intervention import DemarrerInterventionUseCase
from maintenance.application.use_cases.planifier_intervention import PlanifierInterventionUseCase
from maintenance.application.use_cases.retirer_piece import RetirerPieceUseCase
from maintenance.application.use_cases.terminer_intervention import TerminerInterventionUseCase
from maintenance.infrastructure.repositories.django_intervention_repository import (
    DjangoInterventionRepository,
)
from maintenance.infrastructure.repositories.django_piece_detachee_repository import (
    DjangoPieceDetacheeRepository,
)
from maintenance.infrastructure.repositories.django_regle_maintenance_repository import (
    DjangoRegleMaintenanceRepository,
)
from maintenance.infrastructure.repositories.django_technicien_repository import (
    DjangoTechnicienRepository,
)
from maintenance.presentation.serializers.intervention_serializer import (
    InterventionInputSerializer,
    InterventionOutputSerializer,
)
from maintenance.presentation.serializers.piece_detachee_serializer import PieceDetacheeSerializer
from maintenance.presentation.serializers.technicien_serializer import TechnicienSerializer
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository


class InterventionViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant la planification, l'exécution et le suivi financier des interventions.

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'maintenance'
        Le modèle requis est défini dynamiquement selon l'action.
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intervention_repo = DjangoInterventionRepository()
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()
        self.bien_repo = DjangoBienRepository()
        regle_repo = DjangoRegleMaintenanceRepository()
        self.tarif_service = TarificationMaintenanceService(regle_repo)

    # --------------------------------------------------------------------------
    # Mapping action -> modèle pour permissions
    # --------------------------------------------------------------------------
    def get_permissions(self):
        action_model_map = {
            'list': 'intervention',
            'retrieve': 'intervention',
            'create': 'intervention',
            'demarrer': 'intervention',
            'ajouter_piece': 'intervention',
            'terminer': 'intervention',
            'calculer_cout': 'intervention',
            'lister_pieces': 'intervention',
            'lister_techniciens': 'intervention',
            'retirer_piece': 'intervention',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Endpoints
    # --------------------------------------------------------------------------

    def list(self, request):
        """GET /api/maintenance/interventions/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        interventions = self.intervention_repo.find_all(agence_id=agence_id)
        serializer = InterventionOutputSerializer(interventions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """GET /api/maintenance/interventions/{uuid}/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID d'intervention invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée pour votre agence."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InterventionOutputSerializer(intervention)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST /api/maintenance/interventions/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response({"error": "Aucune agence associée à cet utilisateur."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InterventionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        use_case = PlanifierInterventionUseCase(
            self.intervention_repo, self.technicien_repo, self.bien_repo
        )
        try:
            intervention = use_case.execute(
                bien_id=data['bien_id'],
                technicien_id=data['technicien_id'],
                date_debut=data['date_debut'],
                date_fin=data['date_fin'],
                agence_id=agence_id,
            )
            output = InterventionOutputSerializer(intervention).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='demarrer')
    def demarrer(self, request, pk=None):
        """POST /api/maintenance/interventions/{uuid}/demarrer/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée."}, status=status.HTTP_404_NOT_FOUND)

        use_case = DemarrerInterventionUseCase(self.intervention_repo)
        try:
            use_case.execute(intervention_uuid, agence_id=agence_id)
            return Response({"status": "success", "message": "Intervention démarrée avec succès."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='ajouter_piece')
    def ajouter_piece(self, request, pk=None):
        """POST /api/maintenance/interventions/{uuid}/ajouter_piece/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée."}, status=status.HTTP_404_NOT_FOUND)

        piece_id = request.data.get('piece_id')
        quantite = request.data.get('quantite', 1)
        if not piece_id:
            return Response({"error": "Le champ 'piece_id' est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            piece_uuid = UUID(piece_id)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID de pièce invalide."}, status=status.HTTP_400_BAD_REQUEST)

        use_case = AjouterPieceUseCase(self.intervention_repo, self.piece_repo)
        try:
            use_case.execute(intervention_uuid, piece_uuid, int(quantite), agence_id=agence_id)
            return Response({"status": "success", "message": "Pièce ajoutée à l'intervention."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        """POST /api/maintenance/interventions/{uuid}/terminer/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée."}, status=status.HTTP_404_NOT_FOUND)

        use_case = TerminerInterventionUseCase(self.intervention_repo, self.tarif_service)
        try:
            cout_total = use_case.execute(intervention_uuid, agence_id, date.today())
            return Response({"status": "success", "cout_total": cout_total}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='cout')
    def calculer_cout(self, request, pk=None):
        """GET /api/maintenance/interventions/{uuid}/cout/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée."}, status=status.HTTP_404_NOT_FOUND)

        use_case = CalculerCoutInterventionUseCase(self.intervention_repo)
        try:
            cout = use_case.execute(intervention_uuid, agence_id=agence_id)
            return Response({"cout_total": float(cout.valeur)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='pieces')
    def lister_pieces(self, request):
        """GET /api/maintenance/interventions/pieces/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)
        pieces = self.piece_repo.find_all(agence_id=agence_id)
        serializer = PieceDetacheeSerializer(pieces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='techniciens')
    def lister_techniciens(self, request):
        """GET /api/maintenance/interventions/techniciens/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)
        techniciens = self.technicien_repo.get_all(agence_id=agence_id)
        serializer = TechnicienSerializer(techniciens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='pieces/(?P<piece_id>[^/.]+)')
    def retirer_piece(self, request, pk=None, piece_id=None):
        """DELETE /api/maintenance/interventions/{uuid}/pieces/{piece_uuid}/"""
        agence_id = self.get_agence_id()
        try:
            intervention_uuid = UUID(pk)
            piece_uuid = UUID(piece_id)
        except (ValueError, TypeError):
            return Response({"error": "UUID d'intervention ou de pièce invalide."}, status=status.HTTP_400_BAD_REQUEST)

        intervention = self.intervention_repo.get(intervention_uuid, agence_id=agence_id)
        if not intervention:
            return Response({"error": "Intervention non trouvée ou non autorisée."}, status=status.HTTP_404_NOT_FOUND)

        use_case = RetirerPieceUseCase(self.intervention_repo, self.piece_repo)
        try:
            use_case.execute(intervention_uuid, piece_uuid, agence_id=agence_id)
            return Response({"status": "success", "message": "Pièce retirée avec succès."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)