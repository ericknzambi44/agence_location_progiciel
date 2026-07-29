"""
Module de Présentation - Tarification (Clean Architecture / DDD)

Expose la gestion des règles de tarification dynamique pour le module Location.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from location.application.services.tarification_service import TarificationService
from location.domain.entities.regle_tarification import ReglesTarification
from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle
from location.infrastructure.repositories.django_regle_tarification_repository import (
    DjangoRegleTarificationRepository,
)
from location.presentation.serializers.tarification_serializers import (
    RegleTarificationInputSerializer,
    RegleTarificationOutputSerializer,
)


class TarificationViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant la configuration des règles de tarification dynamique des locations.

    Attributs DDD / RBAC :
        permission_classes: Validation RBAC sur les modèles de tarification.
        required_module: Module applicatif 'location'.
        required_model: Modèle de tarification ciblé 'regletarificationmodel'.
    """

    permission_classes = [HasModulePermission]
    required_module = 'location'
    required_model = 'regletarificationmodel'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection des dépendances d'infrastructure et de service du domaine
        self.repo = DjangoRegleTarificationRepository()
        self.service = TarificationService(self.repo)

    def list(self, request):
        """
        Récupère l'ensemble des règles de tarification actives pour l'agence de l'utilisateur.

        Permission requise : location.view_regletarificationmodel
        """
        agence_id = self.get_agence_id()

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre ou remplace la grille tarifaire pour l'agence de l'utilisateur.

        Permission requise : location.add_regletarificationmodel
        """
        agence_id = self.get_agence_id()

        serializer = RegleTarificationInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données de tarification invalides.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        regles_data = serializer.validated_data['regles']

        # Reconstruction des Value Objects du Domaine
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
                active=r.get('active', True),
            )
            regles_obj.append(regle)

        # Création de l'agrégat du domaine et persistance via le service
        regles_aggregat = ReglesTarification(agence_id=agence_id, regles=regles_obj)
        self.service.sauvegarder_regles(regles_aggregat)

        # Retourne la grille mise à jour
        regles_mises_a_jour = self.service.get_regles(agence_id=agence_id)
        output = RegleTarificationOutputSerializer(regles_mises_a_jour.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)