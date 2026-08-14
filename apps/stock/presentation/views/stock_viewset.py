"""
Module de Présentation - Gestion des Stocks (Clean Architecture / DDD)

Expose la consultation des niveaux de stock et l'enregistrement des mouvements.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence
via AgenceMixin : l'agence de l'utilisateur est automatiquement déduite.
"""

from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from stock.application.use_cases.ajuster_stock import AjusterStockUseCase
from stock.infrastructure.repositories.django_mouvement_stock_repository import DjangoMouvementStockRepository
from stock.infrastructure.repositories.django_stock_repository import DjangoStockRepository
from stock.presentation.serializers.stock_serializer import (
    MouvementStockInputSerializer,
    MouvementStockOutputSerializer,
    NiveauStockOutputSerializer,
)


class StockViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant les niveaux de stock et l'historique des mouvements.

    RBAC :
        permission_classes : HasModulePermission
        required_module    : 'stock'
        Modèle cible : 'mouvementstock' pour toutes les actions.
    """

    permission_classes = [HasModulePermission]
    required_module = 'stock'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_repo = DjangoStockRepository()
        self.mouvement_repo = DjangoMouvementStockRepository()

    # --------------------------------------------------------------------------
    # Définition automatique du modèle pour la permission RBAC
    # --------------------------------------------------------------------------
    def get_permissions(self):
        """
        Toutes les actions de ce ViewSet concernent le modèle 'mouvementstock'.
        """
        action_model_map = {
            'list': 'mouvementstock',
            'niveau_article': 'mouvementstock',
            'lister_mouvements': 'mouvementstock',
            'create': 'mouvementstock',
        }
        if self.action in action_model_map:
            self.required_model = action_model_map[self.action]
        return super().get_permissions()

    # --- CONSULTATION DES NIVEAUX DE STOCK ---

    def list(self, request):
        """
        GET /api/stock/stock/
        Consulte les niveaux de stock de tous les articles de l'agence.

        Permission requise : stock.view_mouvementstock
        """
        agence_id = self.get_agence_id()
        stocks = self.stock_repo.get_niveaux_stock(agence_id=agence_id)
        serializer = NiveauStockOutputSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='niveau')
    def niveau_article(self, request, pk=None):
        """
        GET /api/stock/stock/{article_uuid}/niveau/
        Niveau de stock d'un article de l'agence.

        Permission requise : stock.view_mouvementstock
        """
        agence_id = self.get_agence_id()
        try:
            article_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'article invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantite = self.stock_repo.get_quantite_disponible(
            article_id=article_uuid, agence_id=agence_id
        )
        return Response(
            {"article_id": str(article_uuid), "quantite_disponible": quantite},
            status=status.HTTP_200_OK,
        )

    # --- HISTORIQUE DES MOUVEMENTS DE STOCK ---

    @action(detail=False, methods=['get'], url_path='mouvements')
    def lister_mouvements(self, request):
        """
        GET /api/stock/stock/mouvements/
        Journal des mouvements de stock de l'agence.

        Permission requise : stock.view_mouvementstock
        """
        agence_id = self.get_agence_id()
        mouvements = self.mouvement_repo.get_all(agence_id=agence_id)
        serializer = MouvementStockOutputSerializer(mouvements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- CRÉATION DE MOUVEMENT / AJUSTEMENT ---

    def create(self, request):
        """
        POST /api/stock/stock/
        Enregistre un mouvement de stock (entrée, sortie, ajustement)
        pour l'agence de l'utilisateur.

        Permission requise : stock.add_mouvementstock
        """
        agence_id = self.get_agence_id()
        if agence_id is None:
            return Response(
                {"error": "Aucune agence associée à cet utilisateur."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MouvementStockInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        use_case = AjusterStockUseCase(
            stock_repo=self.stock_repo,
            mouvement_repo=self.mouvement_repo,
        )

        try:
            mouvement = use_case.execute(
                article_id=data['article_id'],
                type_mouvement=data['type_mouvement'],
                quantite=data['quantite'],
                motif=data.get('motif', ''),
                user_id=request.user.id,
                agence_id=agence_id,
            )
            output = MouvementStockOutputSerializer(mouvement).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)