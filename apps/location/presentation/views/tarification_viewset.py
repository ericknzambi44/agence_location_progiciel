"""
ViewSet pour la gestion des règles de tarification.
Toutes les opérations sont filtrées par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from uuid import UUID

from config.mixins import AgenceMixin

from location.application.services.tarification_service import TarificationService
from location.infrastructure.repositories.django_regle_tarification_repository import (
    DjangoRegleTarificationRepository
)
from location.presentation.serializers.tarification_serializers import (
    RegleTarificationInputSerializer,
    RegleTarificationOutputSerializer
)
from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle
from location.domain.entities.regle_tarification import ReglesTarification


class TarificationViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet pour la tarification dynamique des locations.
    - GET /tarification/  → liste les règles actuelles (filtrées par agence)
    - POST /tarification/ → enregistre de nouvelles règles (pour l'agence)
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleTarificationRepository()
        self.service = TarificationService(self.repo)

    def list(self, request):
        """
        Récupère les règles de tarification pour l'agence de l'utilisateur.
        """
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre les règles de tarification pour l'agence de l'utilisateur.
        Remplace les règles existantes par les nouvelles.
        """
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        # Validation des données d'entrée avec affichage des erreurs détaillées
        serializer = RegleTarificationInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        regles_data = serializer.validated_data['regles']

        # Construction des objets du domaine
        regles_obj = []
        for r in regles_data:
            regle = RegleTarification(
                type=TypeRegle(r['type']),
                valeur=r['valeur'],
                duree_min=r['duree_min'],
                duree_max=r.get('duree_max'),
                bien_id=r.get('bien_id'),
                categorie_id=r.get('categorie_id'),
                periode_debut=r.get('periode_debut'),
                periode_fin=r.get('periode_fin'),
                description=r.get('description', ''),
                active=r.get('active', True)
            )
            regles_obj.append(regle)

        # Créer l'agrégat et sauvegarder
        regles_aggregat = ReglesTarification(agence_id=agence_id, regles=regles_obj)
        self.service.sauvegarder_regles(regles_aggregat)

        # Retourner la liste mise à jour
        regles = self.service.get_regles(agence_id=agence_id)
        output = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)