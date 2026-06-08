from click import UUID
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from apps.stock.domain.value_objects import quantite
from maintenance.presentation.serializers.intervention_serializer import PlanifierInterventionInputDTO, InterventionOutputDTO
from maintenance.application.use_cases.planifier_intervention import PlanifierInterventionUseCase
from maintenance.application.use_cases.demarrer_intervention import DemarrerInterventionUseCase
from maintenance.application.use_cases.ajouter_piece import AjouterPieceUseCase
from maintenance.application.use_cases.terminer_intervention import TerminerInterventionUseCase
from maintenance.infrastructure.repositories.django_intervention_repository import DjangoInterventionRepository
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository
from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository

class InterventionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.intervention_repo = DjangoInterventionRepository()
        self.technicien_repo = DjangoTechnicienRepository()
        self.bien_repo = DjangoBienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()

    def create(self, request):
        serializer = PlanifierInterventionInputDTO(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        use_case = PlanifierInterventionUseCase(self.intervention_repo, self.technicien_repo, self.bien_repo)
        try:
            intervention = use_case.execute(
                bien_id=data['bien_id'],
                technicien_id=data['technicien_id'],
                debut=data['date_debut'],
                fin=data['date_fin'],
                description_panne=data.get('description_panne', '')
            )
            output = InterventionOutputDTO.from_entity(intervention)
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def demarrer(self, request, pk=None):
        use_case = DemarrerInterventionUseCase(self.intervention_repo)
        try:
            use_case.execute(pk)
            return Response({"status": "démarrée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def ajouter_piece(self, request, pk=None):
        piece_id = request.data.get('piece_id')
        quantite = request.data.get('quantite', 1)
        if not piece_id:
            return Response({"error": "piece_id requis"}, status=400)
        use_case = AjouterPieceUseCase(self.intervention_repo, self.piece_repo)
        try:
            use_case.execute(pk, piece_id, quantite)
            return Response({"status": "pièce ajoutée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        rapport = request.data.get('rapport', '')
        use_case = TerminerInterventionUseCase(self.intervention_repo)
        try:
            use_case.execute(pk, rapport)
            return Response({"status": "terminée"})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
    @action(detail=True, methods=['post'])
    def ajouter_piece(self, request, pk=None):
      piece_id = request.data.get('piece_id')
      quantite = request.data.get('quantite', 1)
      if not piece_id:
        return Response({"error": "piece_id requis"}, status=400)
      use_case = AjouterPieceUseCase(self.intervention_repo, self.piece_repo)
      try:
        use_case.execute(pk, UUID(piece_id), int(quantite))
        return Response({"status": "pièce ajoutée"})
      except ValueError as e:
        return Response({"error": str(e)}, status=400)   