from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from datetime import date
from uuid import UUID
from rh.presentation.views.bien_serializer import BienInputSerializer, BienOutputSerializer
from stock.application.use_cases.creer_bien import CreerBienUseCase
from stock.application.use_cases.verifier_disponibilite import VerifierDisponibiliteUseCase
from stock.application.use_cases.changer_etat_bien import ChangerEtatBienUseCase
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository

class BienViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bien_repo = DjangoBienRepository()

    def create(self, request):
        serializer = BienInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uc = CreerBienUseCase(self.bien_repo)
        try:
            bien = uc.execute(
                reference=data['reference'],
                nom=data['nom'],
                description=data.get('description', ''),
                prix=data['prix_unitaire_ht'],
                date_achat=data.get('date_achat')
            )
            output = BienOutputSerializer.from_entity(bien)
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Méthode list ajoutée
    def list(self, request):
        biens = self.bien_repo.find_all()
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data)

    # Méthode retrieve ajoutée
    def retrieve(self, request, pk=None):
        bien = self.bien_repo.get(UUID(pk))
        if not bien:
            return Response({"error": "Bien introuvable"}, status=status.HTTP_404_NOT_FOUND)
        return Response(BienOutputSerializer.from_entity(bien))

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        if not debut or not fin:
            return Response({"error": "Paramètres debut et fin requis"}, status=400)
        try:
            d1 = date.fromisoformat(debut)
            d2 = date.fromisoformat(fin)
        except ValueError:
            return Response({"error": "Format de date invalide (YYYY-MM-DD)"}, status=400)
        use_case = VerifierDisponibiliteUseCase(self.bien_repo)
        biens = use_case.execute(d1, d2)
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data)

    @action(detail=True, methods=['patch'])
    def changer_etat(self, request, pk=None):
        nouvel_etat = request.data.get('etat')
        if not nouvel_etat:
            return Response({"error": "Etat requis"}, status=400)
        use_case = ChangerEtatBienUseCase(self.bien_repo)
        try:
            use_case.execute(UUID(pk), nouvel_etat)
            return Response({"status": "ok"})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)