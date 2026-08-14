"""
Mapper pour MouvementStock.
"""

from stock.domain.entities.mouvement_stock import MouvementStock
from stock.domain.value_objects.type_mouvement import TypeMouvement
from stock.infrastructure.models import MouvementStock as MouvementStockModel


class MouvementStockMapper:
    @staticmethod
    def to_domain(model: MouvementStockModel) -> MouvementStock:
        return MouvementStock(
            id=model.id,
            article_id=model.bien_id,
            type_mouvement=TypeMouvement(model.type_mouvement),
            quantite=model.quantite,
            motif=model.commentaire or "",
            date_heure=model.date_heure,
        )

    @staticmethod
    def to_model(entity: MouvementStock) -> MouvementStockModel:
        return MouvementStockModel(
            id=entity.id,
            bien_id=entity.article_id,
            type_mouvement=entity.type_mouvement.value,
            quantite=entity.quantite,
            commentaire=entity.motif,
            date_heure=entity.date_heure,
        )