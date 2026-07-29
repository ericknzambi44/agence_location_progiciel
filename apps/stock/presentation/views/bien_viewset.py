"""
Module de Présentation - Stock (Clean Architecture / DDD)

Expose les cas d'utilisation de gestion du matériel/biens louables via des endpoints HTTP.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from stock.application.use_cases.changer_etat_bien import ChangerEtatBienUseCase
from stock.application.use_cases.creer_bien import CreerBienUseCase
from stock.application.use_cases.verifier_disponibilite import VerifierDisponibiliteUseCase
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository
from stock.presentation.serializers.bien_serializer import (
    BienInputSerializer,
    BienOutputSerializer,
)


class BienViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant le cycle de vie des biens (Stock).

    Attributs DDD / RBAC :
        permission_classes: Exige un utilisateur actif disposant des droits sur le module Stock.
        required_module: Module applicatif ciblé pour le RBAC ('stock').
        required_model: Modèle du domaine ciblé ('bienmodel').
    """

    permission_classes = [HasModulePermission]
    required_module = 'stock'
    required_model = 'bienmodel'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection de dépendance du repository d'infrastructure
        self.bien_repo = DjangoBienRepository()

    def create(self, request):
        """
        Crée un nouveau bien dans le stock de l'agence de l'utilisateur.

        Permission requise : stock.add_bienmodel
        """
        agence_id = self.get_agence_id()

        serializer = BienInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Exécution du Cas d'Utilisation (Domain Logic)
        use_case = CreerBienUseCase(self.bien_repo)
        try:
            bien = use_case.execute(
                reference=data['reference'],
                nom=data['nom'],
                description=data.get('description', ''),
                prix=data['prix_unitaire_ht'],
                currency=data.get('devise', 'USD'),
                date_achat=data.get('date_achat'),
                agence_id=agence_id,
            )
            output = BienOutputSerializer.from_entity(bien)
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Récupère la liste de tous les biens rattachés à l'agence de l'utilisateur.

        Permission requise : stock.view_bienmodel
        """
        agence_id = self.get_agence_id()

        biens = self.bien_repo.find_all(agence_id=agence_id)
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Récupère les détails d'un bien spécifique par son UUID.

        Permission requise : stock.view_bienmodel
        """
        agence_id = self.get_agence_id()

        try:
            bien_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bien = self.bien_repo.get(bien_uuid, agence_id=agence_id)
        if not bien:
            return Response(
                {"error": "Bien introuvable ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(BienOutputSerializer.from_entity(bien), status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        """
        Filtre les biens disponibles sur une plage de dates donnée.

        Query Params:
            debut (str): Date au format YYYY-MM-DD
            fin (str): Date au format YYYY-MM-DD

        Permission requise : stock.view_bienmodel
        """
        agence_id = self.get_agence_id()

        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        if not debut or not fin:
            return Response(
                {"error": "Les paramètres 'debut' et 'fin' sont requis (format YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            d1 = date.fromisoformat(debut)
            d2 = date.fromisoformat(fin)
        except ValueError:
            return Response(
                {"error": "Format de date invalide. Utilisez le format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Exécution du Use Case de vérification de disponibilité
        use_case = VerifierDisponibiliteUseCase(self.bien_repo)
        biens = use_case.execute(d1, d2, agence_id=agence_id)
        data = [BienOutputSerializer.from_entity(b) for b in biens]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='changer_etat')
    def changer_etat(self, request, pk=None):
        """
        Met à jour l'état opérationnel d'un bien (ex: EN_MAINTENANCE, DISPONIBLE).

        Payload:
            etat (str): Le nouvel état à appliquer.

        Permission requise : stock.change_bienmodel
        """
        agence_id = self.get_agence_id()

        nouvel_etat = request.data.get('etat')
        if not nouvel_etat:
            return Response(
                {"error": "Le champ 'etat' est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bien_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bien = self.bien_repo.get(bien_uuid, agence_id=agence_id)
        if not bien:
            return Response(
                {"error": "Bien introuvable ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        use_case = ChangerEtatBienUseCase(self.bien_repo)
        try:
            use_case.execute(bien_uuid, nouvel_etat)
            return Response(
                {"status": "success", "message": f"État mis à jour vers '{nouvel_etat}'."},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)