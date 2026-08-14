"""
Module de Présentation - Stock (Clean Architecture / DDD)

Expose les endpoints de gestion des biens louables.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence
via AgenceMixin : l'agence de l'utilisateur est automatiquement déduite
de son employé lié, sans jamais être demandée dans le payload.
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
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

    RBAC :
        permission_classes : vérifie que l'utilisateur a la permission requise
        required_module    : 'stock'
        La méthode get_permissions() définit automatiquement le modèle
        requis pour chaque action (toujours 'bien' ici).
    """

    permission_classes = [HasModulePermission]
    required_module = 'stock'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bien_repo = DjangoBienRepository()

    # --------------------------------------------------------------------------
    # Définition automatique du modèle pour la permission RBAC
    # --------------------------------------------------------------------------
    def get_permissions(self):
        """
        Associe chaque action au nom de modèle Django attendu par la permission.
        Ici tout est lié au modèle 'bien'.
        """
        action_model_map = {
            'create': 'bien',
            'list': 'bien',
            'retrieve': 'bien',
            'disponibles': 'bien',
            'changer_etat': 'bien',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --------------------------------------------------------------------------
    # Endpoints
    # --------------------------------------------------------------------------

    def create(self, request):
        """
        POST /api/stock/biens/
        Crée un nouveau bien dans le stock de l'agence de l'utilisateur.

        L'agence est automatiquement déduite de l'employé lié à l'utilisateur.
        Permission requise : stock.add_bien
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BienInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

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
            output = BienOutputSerializer(bien).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        GET /api/stock/biens/
        Liste tous les biens de l'agence de l'utilisateur.

        Permission requise : stock.view_bien
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response([], status=status.HTTP_200_OK)

        biens = self.bien_repo.find_all(agence_id=agence_id)
        serializer = BienOutputSerializer(biens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /api/stock/biens/{uuid}/
        Détail d'un bien appartenant à l'agence de l'utilisateur.

        Permission requise : stock.view_bien
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

        serializer = BienOutputSerializer(bien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        """
        GET /api/stock/biens/disponibles/?debut=YYYY-MM-DD&fin=YYYY-MM-DD
        Liste les biens disponibles sur une période, filtrés par agence.

        Permission requise : stock.view_bien
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

        use_case = VerifierDisponibiliteUseCase(self.bien_repo)
        biens = use_case.execute(d1, d2, agence_id=agence_id)
        serializer = BienOutputSerializer(biens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='changer_etat')
    def changer_etat(self, request, pk=None):
        """
        PATCH /api/stock/biens/{uuid}/changer_etat/
        Change l'état d'un bien, en s'assurant qu'il appartient à l'agence.

        Permission requise : stock.change_bien
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

        # Vérification préalable que le bien appartient à l'agence
        bien = self.bien_repo.get(bien_uuid, agence_id=agence_id)
        if not bien:
            return Response(
                {"error": "Bien introuvable ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        use_case = ChangerEtatBienUseCase(self.bien_repo)
        try:
            use_case.execute(bien_uuid, nouvel_etat, agence_id=agence_id)
            return Response(
                {"status": "success", "message": f"État mis à jour vers '{nouvel_etat}'."},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)