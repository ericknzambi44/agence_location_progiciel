"""
ViewSet pour le module Location.
Gère les clients, les contrats et le calcul du montant avec tarification dynamique.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID
from datetime import date

from location.application.use_cases.creer_client import CreerClientUseCase
from location.application.use_cases.louer_bien import LouerBienUseCase
from location.application.use_cases.retourner_bien import RetournerBienUseCase
from location.application.use_cases.consulter_contrats import ConsulterContratsUseCase
from location.application.use_cases.calculer_montant import CalculerMontantLocationUseCase
from location.application.services.tarification_service import TarificationService

from location.infrastructure.repositories.django_client_repository import DjangoClientRepository
from location.infrastructure.repositories.django_contrat_repository import DjangoContratRepository
from location.infrastructure.repositories.django_regle_tarification_repository import (
    DjangoRegleTarificationRepository
)
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository
from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository

from location.presentation.serializers.location_serializers import (
    ClientInputSerializer,
    ClientOutputSerializer,
    ContratInputSerializer,
    ContratOutputSerializer,
)


class LocationViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion des locations.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_repo = DjangoClientRepository()
        self.contrat_repo = DjangoContratRepository()
        self.bien_repo = DjangoBienRepository()
        # Service de tarification
        regle_repo = DjangoRegleTarificationRepository()
        self.tarif_service = TarificationService(regle_repo)

    def _get_agence_id(self):
        """Récupère l'ID de la première agence active."""
        agence_repo = DjangoAgenceRepository()
        agences = agence_repo.list_actives()
        if not agences:
            raise ValueError("Aucune agence active trouvée.")
        return agences[0].id

    # --------------------------------------------------------------
    #  CLIENTS
    # --------------------------------------------------------------

    def create_client(self, request):
        """
        POST /location/clients/
        Crée un nouveau client.
        """
        serializer = ClientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uc = CreerClientUseCase(self.client_repo)
        try:
            client = uc.execute(**serializer.validated_data)
            output = ClientOutputSerializer(client).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list_clients(self, request):
        """
        GET /location/clients/
        Liste tous les clients.
        """
        clients = self.client_repo.list_all()
        serializer = ClientOutputSerializer(clients, many=True)
        return Response(serializer.data)

    # --------------------------------------------------------------
    #  CONTRATS
    # --------------------------------------------------------------

    def create_contrat(self, request):
        """
        POST /location/contrats/
        Crée un contrat de location avec calcul dynamique du montant.
        """
        serializer = ContratInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            agence_id = self._get_agence_id()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        uc = LouerBienUseCase(
            self.contrat_repo,
            self.client_repo,
            self.bien_repo,
            self.tarif_service
        )
        try:
            contrat = uc.execute(
                client_id=data['client_id'],
                bien_id=data['bien_id'],
                agence_id=agence_id,
                date_debut=data['date_debut'],
                date_fin=data['date_fin']
            )
            output = ContratOutputSerializer(contrat).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list_contrats(self, request):
        """
        GET /location/contrats/
        Liste les contrats actifs.
        """
        uc = ConsulterContratsUseCase(self.contrat_repo)
        contrats = uc.execute()
        serializer = ContratOutputSerializer(contrats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        GET /location/contrats/{id}/
        Détail d'un contrat.
        """
        contrat = self.contrat_repo.get(pk)  # pk est déjà un UUID
        if not contrat:
            return Response({"error": "Contrat non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContratOutputSerializer(contrat)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='retourner')
    def retourner(self, request, pk=None):
        """
        POST /location/contrats/{id}/retourner/
        Termine un contrat actif.
        """
        uc = RetournerBienUseCase(self.contrat_repo)
        try:
            uc.execute(pk)  # pk est déjà un UUID
            return Response({"status": "contrat terminé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --------------------------------------------------------------
    #  CALCUL DU MONTANT ESTIMÉ
    # --------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='calculer-montant')
    def calculer_montant(self, request):
        """
        POST /location/calculer-montant/
        Estime le montant d'une location avant création du contrat.
        Body: {"bien_id": "...", "date_debut": "YYYY-MM-DD", "date_fin": "YYYY-MM-DD"}
        """
        bien_id = request.data.get('bien_id')
        date_debut = request.data.get('date_debut')
        date_fin = request.data.get('date_fin')

        if not bien_id or not date_debut or not date_fin:
            return Response(
                {"error": "bien_id, date_debut et date_fin sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            debut = date.fromisoformat(date_debut)
            fin = date.fromisoformat(date_fin)
        except ValueError:
            return Response(
                {"error": "Format de date invalide. Utiliser YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            agence_id = self._get_agence_id()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        uc = CalculerMontantLocationUseCase(self.bien_repo, self.tarif_service)
        try:
            montant = uc.execute(UUID(bien_id), agence_id, debut, fin)
            return Response({"montant_total": float(montant.valeur)})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)