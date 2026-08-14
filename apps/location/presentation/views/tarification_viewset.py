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

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'location'
        Modèle requis : 'regletarification' pour toutes les actions.
    """

    permission_classes = [HasModulePermission]
    required_module = 'location'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleTarificationRepository()
        self.service = TarificationService(self.repo)

    # --------------------------------------------------------------------------
    # Mapping action -> modèle pour permissions RBAC
    # --------------------------------------------------------------------------
    def get_permissions(self):
        """
        Toutes les actions concernent le modèle 'regletarification'.
        """
        action_model_map = {
            'list': 'regletarification',
            'create': 'regletarification',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Endpoints
    # --------------------------------------------------------------------------

    def list(self, request):
        """
        GET /api/location/tarification/
        Récupère l'ensemble des règles de tarification actives pour l'agence.

        Permission requise : location.view_regletarification
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        regles = self.service.get_regles(agence_id=agence_id)
        serializer = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST /api/location/tarification/
        Enregistre ou remplace la grille tarifaire pour l'agence.

        Permission requise : location.add_regletarification
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegleTarificationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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