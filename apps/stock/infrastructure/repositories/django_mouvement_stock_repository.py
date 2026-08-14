"""
Repository Django pour les mouvements de stock.
"""

from typing import List
from uuid import UUID

from stock.domain.repositories.mouvement_stock_repository import MouvementStockRepository
from stock.domain.entities.mouvement_stock import MouvementStock
from stock.infrastructure.models import MouvementStock as MouvementStockModel
from stock.infrastructure.mappers.mouvement_stock_mapper import MouvementStockMapper


class DjangoMouvementStockRepository(MouvementStockRepository):
    """
    Implémentation ORM du repository des mouvements.
    """

    def add(self, mouvement: MouvementStock) -> None:
        """
        Enregistre un mouvement.
        """
        model = MouvementStockMapper.to_model(mouvement)
        model.save()
        mouvement.id = model.id

    def get_all(self, agence_id: UUID = None) -> List[MouvementStock]:
        """
        Retourne tous les mouvements, filtrés par agence.
        """
        qs = MouvementStockModel.objects.all()
        if agence_id is not None:
            qs = qs.filter(bien__agence_id=agence_id)
        return [MouvementStockMapper.to_domain(m) for m in qs]