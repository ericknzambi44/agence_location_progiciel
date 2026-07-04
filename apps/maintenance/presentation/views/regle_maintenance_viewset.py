"""
ViewSet pour la gestion des règles de tarification de maintenance.
Toutes les opérations sont filtrées par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from uuid import UUID

from config.mixins import AgenceMixin

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


class RegleMaintenanceViewSet(AgenceMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleMaintenanceRepository()
        self.service = TarificationMaintenanceService(self.repo)

    def list(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

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
                active=r.get('active', True)
            )
            regles_obj.append(regle)

        regles_aggregat = ReglesMaintenance(agence_id=agence_id, regles=regles_obj)
        self.service.sauvegarder_regles(regles_aggregat)

        regles = self.service.get_regles(agence_id=agence_id)
        output = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)