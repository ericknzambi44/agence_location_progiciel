"""
Module de Présentation - Règles de Tarification Maintenance (Clean Architecture / DDD)

Expose la gestion des règles de tarification de la maintenance par agence.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from maintenance.application.services.tarification_maintenance_service import (
    TarificationMaintenanceService,
)
from maintenance.domain.entities.regle_maintenance import ReglesMaintenance
from maintenance.domain.value_objects.regle_maintenance import (
    RegleMaintenance,
    TypeRegleMaintenance,
)
from maintenance.infrastructure.repositories.django_regle_maintenance_repository import (
    DjangoRegleMaintenanceRepository,
)
from maintenance.presentation.serializers.regle_maintenance_serializer import (
    RegleMaintenanceInputSerializer,
    RegleMaintenanceOutputSerializer,
)


class RegleMaintenanceViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant la configuration des règles de tarification de la maintenance.

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'maintenance'
        Modèle requis : 'reglemaintenance'
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleMaintenanceRepository()
        self.service = TarificationMaintenanceService(self.repo)

    # --------------------------------------------------------------------------
    # Mapping action -> modèle pour permissions
    # --------------------------------------------------------------------------
    def get_permissions(self):
        action_model_map = {
            'list': 'reglemaintenance',
            'create': 'reglemaintenance',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Endpoints
    # --------------------------------------------------------------------------

    def list(self, request):
        """GET /api/maintenance/regles/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response({"error": "Aucune agence associée à cet utilisateur."}, status=status.HTTP_400_BAD_REQUEST)

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST /api/maintenance/regles/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response({"error": "Aucune agence associée à cet utilisateur."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegleMaintenanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regles_data = serializer.validated_data['regles']

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
                active=r.get('active', True),
            )
            regles_obj.append(regle)

        regles_aggregat = ReglesMaintenance(agence_id=agence_id, regles=regles_obj)
        self.service.sauvegarder_regles(regles_aggregat)

        regles_a_jour = self.service.get_regles(agence_id=agence_id)
        output = RegleMaintenanceOutputSerializer(regles_a_jour.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)