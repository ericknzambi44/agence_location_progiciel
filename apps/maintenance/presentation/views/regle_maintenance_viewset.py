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

    Attributs DDD / RBAC :
        permission_classes: Validation RBAC sur le module Maintenance.
        required_module: Module applicatif ciblé ('maintenance').
        required_model: Modèle de domaine ciblé ('reglemaintenancemodel').
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'
    required_model = 'reglemaintenancemodel'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection du repository et du service de tarification
        self.repo = DjangoRegleMaintenanceRepository()
        self.service = TarificationMaintenanceService(self.repo)

    def list(self, request):
        """
        Récupère l'ensemble des règles de tarification de maintenance de l'agence.

        Permission requise : maintenance.view_reglemaintenancemodel
        """
        agence_id = self.get_agence_id()

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleMaintenanceOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre ou met à jour la grille des règles de tarification de maintenance.

        Permission requise : maintenance.add_reglemaintenancemodel
        """
        agence_id = self.get_agence_id()

        serializer = RegleMaintenanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regles_data = serializer.validated_data['regles']

        # Reconstruction des Value Objects du Domaine
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

        # Instanciation de l'agrégat du domaine et persistance
        regles_aggregat = ReglesMaintenance(agence_id=agence_id, regles=regles_obj)
        self.service.sauvegarder_regles(regles_aggregat)

        # Récupération et retour de la liste à jour
        regles_a_jour = self.service.get_regles(agence_id=agence_id)
        output = RegleMaintenanceOutputSerializer(regles_a_jour.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)