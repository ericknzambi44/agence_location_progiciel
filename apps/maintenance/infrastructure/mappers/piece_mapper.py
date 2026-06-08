from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import PieceDetacheeModel

class PieceDetacheeMapper:
    @staticmethod
    def to_domain(model: PieceDetacheeModel) -> PieceDetachee:
        return PieceDetachee(
            id=model.id,
            reference=model.reference,
            nom=model.nom,
            prix_unitaire=model.prix_unitaire,
            stock=model.stock
        )

    @staticmethod
    def to_model(entity: PieceDetachee) -> PieceDetacheeModel:
        return PieceDetacheeModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            prix_unitaire=entity.prix_unitaire,
            stock=entity.stock
        )