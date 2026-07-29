"""
Module de Présentation - Techniciens (Clean Architecture / DDD)

Expose la gestion de l'annuaire des techniciens de maintenance par agence.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from decimal import Decimal

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

    Attributs DDD / RBAC :
        permission_classes: Validation RBAC sur le module Maintenance.
        required_module: Module applicatif ciblé ('maintenance').
        required_model: Modèle de domaine ciblé ('technicienmodel').
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'
    required_model = 'technicienmodel'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection du repository des techniciens
        self.repo = DjangoTechnicienRepository()

    def list(self, request):
        """
        Consulte la liste complète des techniciens rattachés à l'agence.

        Permission requise : maintenance.view_technicienmodel
        """
        agence_id = self.get_agence_id()

        techniciens = self.repo.get_all(agence_id=agence_id)
        serializer = TechnicienSerializer(techniciens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre un nouveau technicien pour l'agence.

        Permission requise : maintenance.add_technicienmodel
        """
        agence_id = self.get_agence_id()

        serializer = TechnicienSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        try:
            technicien = Technicien(
                nom=PersonName(data['nom']),
                prenom=PersonName(data['prenom']),
                email=Email(data['email']),
                cout_horaire=Decimal(str(data['cout_horaire'])),
                agence_id=agence_id,
            )
            self.repo.add(technicien)
            output = TechnicienSerializer(technicien).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)