"""
Repository Django pour la gestion des niveaux de stock.

Ce repository calcule le stock disponible à partir des mouvements.
"""

from uuid import UUID

from stock.domain.repositories.stock_repository import StockRepository
from stock.infrastructure.models import Bien, MouvementStock


class DjangoStockRepository(StockRepository):
    """
    Implémentation basée sur l'ORM Django.
    """

    def get_article(self, article_id: UUID, agence_id: UUID = None):
        """
        Récupère un bien (article) par son identifiant.

        Returns:
            Bien ou None si introuvable.
        """
        qs = Bien.objects.filter(id=article_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return qs.first()

    def get_quantite_disponible(self, article_id: UUID, agence_id: UUID = None) -> int:
        """
        Calcule la quantité disponible en sommant les entrées et sorties.
        """
        mouvements = MouvementStock.objects.filter(bien_id=article_id)
        if agence_id is not None:
            mouvements = mouvements.filter(
                bien__agence_id=agence_id
            )

        total = 0
        for m in mouvements:
            if m.type_mouvement in ['entree', 'retour']:
                total += m.quantite
            elif m.type_mouvement in ['sortie']:
                total -= m.quantite
            # Les ajustements sont ignorés ou traités spécifiquement
        return total

    def incrementer_stock(self, article_id: UUID, quantite: int, agence_id: UUID = None) -> None:
        """
        Incrémente le stock en créant un mouvement d'entrée.
        """
        # On suppose que le repository des mouvements est utilisé pour enregistrer le mouvement.
        # Ici on ne fait rien, car le mouvement est déjà enregistré dans AjusterStockUseCase.
        pass

    def decrementer_stock(self, article_id: UUID, quantite: int, agence_id: UUID = None) -> None:
        """
        Décrémente le stock en créant un mouvement de sortie.
        """
        pass