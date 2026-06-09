from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID
from datetime import datetime

from maintenance.application.use_cases.calculer_cout import CalculerCoutInterventionUseCase
from maintenance.presentation.serializers.intervention_serializer import (
    InterventionInputSerializer,
    InterventionOutputSerializer,
    AjoutPieceSerializer,
)
from maintenance.application.use_cases.planifier_intervention import PlanifierInterventionUseCase
from maintenance.application.use_cases.demarrer_intervention import DemarrerInterventionUseCase
from maintenance.application.use_cases.ajouter_piece import AjouterPieceUseCase
from maintenance.application.use_cases.terminer_intervention import TerminerInterventionUseCase

from maintenance.infrastructure.repositories.django_intervention_repository import DjangoInterventionRepository
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository


class InterventionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intervention_repo = DjangoInterventionRepository()
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()
        # plus besoin de self.bien_repo (contournement dans le use case)

    def create(self, request):
        """POST /maintenance/interventions/ - Planifier une intervention"""
        serializer = InterventionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        uc = PlanifierInterventionUseCase(
            self.intervention_repo,
            self.technicien_repo   # bien_repo supprimé
        )
        try:
            intervention = uc.execute(
                bien_id=data['bien_id'],
                technicien_id=data['technicien_id'],
                date_debut=data['date_debut'],
                date_fin=data['date_fin'],
                description_panne=data.get('description_panne', '')
            )
            output = InterventionOutputSerializer.from_entity(intervention)
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='demarrer')
    def demarrer(self, request, pk=None):
        """POST /interventions/{id}/demarrer/"""
        uc = DemarrerInterventionUseCase(self.intervention_repo)
        try:
            uc.execute(UUID(pk))
            return Response({"status": "ok"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='ajouter_piece')
    def ajouter_piece(self, request, pk=None):
        """POST /interventions/{id}/ajouter_piece/"""
        serializer = AjoutPieceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        uc = AjouterPieceUseCase(self.intervention_repo, self.piece_repo)
        try:
            uc.execute(UUID(pk), data['piece_id'], data['quantite'])
            return Response({"status": "pièce ajoutée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        """POST /interventions/{id}/terminer/"""
        uc = TerminerInterventionUseCase(self.intervention_repo)
        try:
            result = uc.execute(UUID(pk))
            return Response({"status": "ok", "cout_total": result})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='cout')
    def cout(self, request, pk=None):
        """GET /interventions/{id}/cout/"""
        uc = CalculerCoutInterventionUseCase(self.intervention_repo)
        try:
            details = uc.execute(UUID(pk))
            return Response(details)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)