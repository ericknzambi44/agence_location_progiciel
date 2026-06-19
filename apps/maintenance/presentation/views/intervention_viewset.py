from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID

from maintenance.presentation.serializers.intervention_serializer import (
    InterventionInputSerializer, InterventionOutputSerializer
)
from maintenance.presentation.serializers.technicien_serializer import TechnicienSerializer
from maintenance.presentation.serializers.piece_serializer import PieceDetacheeSerializer
from maintenance.application.use_cases.planifier_intervention import PlanifierInterventionUseCase
from maintenance.application.use_cases.demarrer_intervention import DemarrerInterventionUseCase
from maintenance.application.use_cases.ajouter_piece import AjouterPieceUseCase
from maintenance.application.use_cases.terminer_intervention import TerminerInterventionUseCase
from maintenance.application.use_cases.calculer_cout import CalculerCoutInterventionUseCase
from maintenance.infrastructure.repositories.django_intervention_repository import DjangoInterventionRepository
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository

class InterventionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intervention_repo = DjangoInterventionRepository()
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()
        self.bien_repo = DjangoBienRepository()

    # --- LIST : GET /interventions/ ---
    def list(self, request):
        """Retourne la liste de toutes les interventions."""
        interventions = self.intervention_repo.find_all()
        serializer = InterventionOutputSerializer(interventions, many=True)
        return Response(serializer.data)

    # --- RETRIEVE : GET /interventions/{id}/ ---
    def retrieve(self, request, pk=None):
        """Retourne les détails d'une intervention spécifique."""
        intervention = self.intervention_repo.get(UUID(pk))
        if not intervention:
            return Response({"error": "Intervention non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InterventionOutputSerializer(intervention)
        return Response(serializer.data)

    # --- CREATE : POST /interventions/ ---
    def create(self, request):
        serializer = InterventionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uc = PlanifierInterventionUseCase(
            self.intervention_repo,
            self.technicien_repo,
            self.bien_repo
        )
        try:
            intervention = uc.execute(
                bien_id=data['bien_id'],
                technicien_id=data['technicien_id'],
                date_debut=data['date_debut'],
                date_fin=data['date_fin']
            )
            output = InterventionOutputSerializer(intervention).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- DÉMARRER ---
    @action(detail=True, methods=['post'], url_path='demarrer')
    def demarrer(self, request, pk=None):
        uc = DemarrerInterventionUseCase(self.intervention_repo)
        try:
            uc.execute(UUID(pk))
            return Response({"status": "intervention démarrée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- AJOUTER PIÈCE ---
    @action(detail=True, methods=['post'], url_path='ajouter_piece')
    def ajouter_piece(self, request, pk=None):
        piece_id = request.data.get('piece_id')
        quantite = request.data.get('quantite', 1)
        if not piece_id:
            return Response({"error": "piece_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        uc = AjouterPieceUseCase(self.intervention_repo, self.piece_repo)
        try:
            uc.execute(UUID(pk), UUID(piece_id), int(quantite))
            return Response({"status": "pièce ajoutée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- TERMINER ---
    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        uc = TerminerInterventionUseCase(self.intervention_repo)
        try:
            cout_total = uc.execute(UUID(pk))   # retourne float
            return Response({"cout_total": cout_total})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- CALCULER COÛT ---
    @action(detail=True, methods=['get'], url_path='cout', url_name='cout')
    def calculer_cout(self, request, pk=None):
        uc = CalculerCoutInterventionUseCase(self.intervention_repo)
        try:
            cout = uc.execute(UUID(pk))   # retourne un objet Cout
            return Response({"cout_total": float(cout.valeur)})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- LISTE DES PIÈCES ---
    @action(detail=False, methods=['get'], url_path='pieces')
    def lister_pieces(self, request):
        """GET /interventions/pieces/ -> liste toutes les pièces détachées"""
        pieces = self.piece_repo.find_all()
        serializer = PieceDetacheeSerializer(pieces, many=True)
        return Response(serializer.data)

    # --- LISTE DES TECHNICIENS ---
    @action(detail=False, methods=['get'], url_path='techniciens')
    def lister_techniciens(self, request):
        """GET /interventions/techniciens/ -> liste tous les techniciens (pour le sélecteur)"""
        techniciens = self.technicien_repo.get_all()
        serializer = TechnicienSerializer(techniciens, many=True)
        return Response(serializer.data)