"""
Module de Présentation - Techniciens (Clean Architecture / DDD)

Expose la gestion de l'annuaire des techniciens de maintenance par agence.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from decimal import Decimal
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.repositories.django_technicien_repository import (
    DjangoTechnicienRepository,
)
from maintenance.presentation.serializers.technicien_serializer import TechnicienSerializer
from shared_kernel.domain.value_objects import Email, PersonName


class TechnicienViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant l'annuaire et la création des techniciens de maintenance.

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'maintenance'
        Modèle requis : 'technicien'
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoTechnicienRepository()

    # --------------------------------------------------------------------------
    # Mapping action -> modèle pour permissions
    # --------------------------------------------------------------------------
    def get_permissions(self):
        action_model_map = {
            'list': 'technicien',
            'retrieve': 'technicien',
            'create': 'technicien',
            'update': 'technicien',
            'partial_update': 'technicien',
            'destroy': 'technicien',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Endpoints
    # --------------------------------------------------------------------------

    def list(self, request):
        """GET /api/maintenance/techniciens/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        techniciens = self.repo.get_all(agence_id=agence_id)
        serializer = TechnicienSerializer(techniciens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """GET /api/maintenance/techniciens/{uuid}/"""
        agence_id = self.get_agence_id()
        try:
            technicien_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response({"error": "Identifiant UUID de technicien invalide."}, status=status.HTTP_400_BAD_REQUEST)

        technicien = self.repo.get(technicien_uuid, agence_id=agence_id)
        if not technicien:
            return Response({"error": "Technicien non trouvé ou non autorisé."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TechnicienSerializer(technicien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST /api/maintenance/techniciens/"""
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response({"error": "Aucune agence associée à cet utilisateur."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TechnicienSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            technicien = Technicien(
                nom=PersonName(data['nom']),
                prenom=PersonName(data['prenom']),
                email=Email(data['email']),
                cout_horaire=Decimal(str(data['cout_horaire'])),
                agence_id=agence_id,
                est_actif=True,
            )
            self.repo.add(technicien)
            output = TechnicienSerializer(technicien).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)