"""
ViewSet pour la gestion des biens (Stock).
Expose les endpoints CRUD, vérification de disponibilité et changement d'état.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from datetime import date
from uuid import UUID

from stock.application.use_cases.creer_bien import CreerBienUseCase
from stock.application.use_cases.verifier_disponibilite import VerifierDisponibiliteUseCase
from stock.application.use_cases.changer_etat_bien import ChangerEtatBienUseCase
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository
from stock.presentation.serializers.bien_serializer import (
    BienInputSerializer,
    BienOutputSerializer
)


class BienViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion des biens.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bien_repo = DjangoBienRepository()

    # --- CREATE : POST /biens/ ---
    def create(self, request):
        """
        Crée un nouveau bien.
        """
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
                currency=data.get('devise', 'USD'),
                date_achat=data.get('date_achat')
            )
            output = BienOutputSerializer.from_entity(bien)
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- LIST : GET /biens/ ---
    def list(self, request):
        """
        Liste tous les biens.
        """
        biens = self.bien_repo.find_all()
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data)

    # --- RETRIEVE : GET /biens/{id}/ ---
    def retrieve(self, request, pk=None):
        """
        Détail d'un bien.
        """
        bien = self.bien_repo.get(UUID(pk))
        if not bien:
            return Response({"error": "Bien introuvable"}, status=status.HTTP_404_NOT_FOUND)
        return Response(BienOutputSerializer.from_entity(bien))

    # --- DISPONIBILITÉ : GET /biens/disponibles/ ---
    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        """
        Vérifie la disponibilité des biens sur une période donnée.
        Paramètres : debut (YYYY-MM-DD), fin (YYYY-MM-DD)
        """
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')

        if not debut or not fin:
            return Response(
                {"error": "Paramètres 'debut' et 'fin' requis (format YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            d1 = date.fromisoformat(debut)
            d2 = date.fromisoformat(fin)
        except ValueError:
            return Response(
                {"error": "Format de date invalide. Utilisez YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        use_case = VerifierDisponibiliteUseCase(self.bien_repo)
        biens = use_case.execute(d1, d2)
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data)

    # --- CHANGER ÉTAT : PATCH /biens/{id}/changer_etat/ ---
    @action(detail=True, methods=['patch'], url_path='changer_etat')
    def changer_etat(self, request, pk=None):
        """
        Change l'état d'un bien.
        Body : {"etat": "disponible|en_maintenance|endommage|archive"}
        """
        nouvel_etat = request.data.get('etat')
        if not nouvel_etat:
            return Response(
                {"error": "Le champ 'etat' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        use_case = ChangerEtatBienUseCase(self.bien_repo)
        try:
            use_case.execute(UUID(pk), nouvel_etat)
            return Response({"status": "ok"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)