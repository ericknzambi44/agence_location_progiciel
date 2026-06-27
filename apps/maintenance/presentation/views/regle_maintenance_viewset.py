"""
ViewSet pour la gestion des règles de tarification de maintenance.
Expose les endpoints GET et POST /api/maintenance/regles-maintenance/.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID

from maintenance.application.services.tarification_maintenance_service import TarificationMaintenanceService
from maintenance.infrastructure.repositories.django_regle_maintenance_repository import (
    DjangoRegleMaintenanceRepository
)
from maintenance.presentation.serializers.regle_maintenance_serializer import (
    RegleMaintenanceInputSerializer,
    RegleMaintenanceOutputSerializer
)
from maintenance.domain.value_objects.regle_maintenance import RegleMaintenance, TypeRegleMaintenance
from maintenance.domain.entities.regle_maintenance import ReglesMaintenance
from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository


class RegleMaintenanceViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion des règles de tarification de maintenance.
    - GET /regles-maintenance/  → liste les règles actuelles
    - POST /regles-maintenance/ → enregistre de nouvelles règles
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleMaintenanceRepository()
        self.service = TarificationMaintenanceService(self.repo)

    def _get_agence_id(self):
        """Récupère l'ID de la première agence active."""
        agence_repo = DjangoAgenceRepository()
        agences = agence_repo.list_actives()
        if not agences:
            raise ValueError("Aucune agence active trouvée.")
        return agences[0].id

    def list(self, request):
        """
        GET /regles-maintenance/
        Récupère les règles de tarification pour l'agence par défaut.
        """
        try:
            agence_id = self._get_agence_id()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        regles = self.service.get_regles(agence_id)
        serializer = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST /regles-maintenance/
        Enregistre les règles de tarification pour l'agence par défaut.
        Remplace les règles existantes par les nouvelles.
        """
        try:
            agence_id = self._get_agence_id()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        # Validation des données d'entrée
        serializer = RegleMaintenanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regles_data = serializer.validated_data['regles']

        # Construction des objets du domaine
        regles_obj = []
        for r in regles_data:
            regle = RegleMaintenance(
                type=TypeRegleMaintenance(r['type']),
                valeur=r['valeur'],
                agence_id=agence_id,
                duree_min=r['duree_min'],
                duree_max=r.get('duree_max'),
                periode_debut=r.get('periode_debut'),
                periode_fin=r.get('periode_fin'),
                description=r.get('description', ''),
                active=r.get('active', True)
            )
            regles_obj.append(regle)

        # Créer l'agrégat
        regles_aggregat = ReglesMaintenance(agence_id=agence_id, regles=regles_obj)

        # Sauvegarder
        self.service.sauvegarder_regles(regles_aggregat)

        # Retourner la liste mise à jour
        regles = self.service.get_regles(agence_id)
        output = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)