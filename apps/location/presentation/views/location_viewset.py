"""
ViewSet pour le module Location.
Gère les clients, les contrats et le calcul du montant avec tarification dynamique,
avec filtrage par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from uuid import UUID
from datetime import date

from config.mixins import AgenceMixin

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
from location.presentation.serializers.location_serializers import ClientInputSerializer, ClientOutputSerializer, ContratInputSerializer, ContratOutputSerializer
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository


class LocationViewSet(AgenceMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_repo = DjangoClientRepository()
        self.contrat_repo = DjangoContratRepository()
        self.bien_repo = DjangoBienRepository()
        regle_repo = DjangoRegleTarificationRepository()
        self.tarif_service = TarificationService(regle_repo)

    # --- CLIENTS ---
    def create_client(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = ClientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uc = CreerClientUseCase(self.client_repo)
        try:
            client = uc.execute(**serializer.validated_data, agence_id=agence_id)
            output = ClientOutputSerializer(client).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list_clients(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        clients = self.client_repo.list_all(agence_id=agence_id)
        serializer = ClientOutputSerializer(clients, many=True)
        return Response(serializer.data)

    # --- CONTRATS ---
    def create_contrat(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = ContratInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

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
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        uc = ConsulterContratsUseCase(self.contrat_repo)
        contrats = uc.execute(agence_id=agence_id)
        serializer = ContratOutputSerializer(contrats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='retourner')
    def retourner(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        contrat = self.contrat_repo.get(UUID(pk), agence_id=agence_id)
        if not contrat:
            return Response({"error": "Contrat non trouvé ou non autorisé"}, status=status.HTTP_404_NOT_FOUND)

        uc = RetournerBienUseCase(self.contrat_repo)
        try:
            uc.execute(UUID(pk))
            return Response({"status": "contrat terminé"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- CALCUL DU MONTANT ESTIMÉ ---
    @action(detail=False, methods=['post'], url_path='calculer-montant')
    def calculer_montant(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

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

        uc = CalculerMontantLocationUseCase(self.bien_repo, self.tarif_service)
        try:
            montant = uc.execute(UUID(bien_id), agence_id, debut, fin)
            return Response({"montant_total": float(montant.valeur)})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)