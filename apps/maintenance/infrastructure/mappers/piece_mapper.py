"""
Mapper entre l'entité domaine PieceDetachee et le modèle ORM PieceDetacheeModel.
Assure la conversion dans les deux sens, incluant l'agence_id pour le multi-agences.
"""
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import PieceDetacheeModel


class PieceDetacheeMapper:
    """Conversion bidirectionnelle pour les pièces détachées."""

    @staticmethod
    def to_domain(model: PieceDetacheeModel) -> PieceDetachee:
        """
        Construit une entité domaine à partir du modèle Django.
        """
        return PieceDetachee(
            id=model.id,
            reference=model.reference,
            nom=model.nom,
            prix_unitaire=model.prix_unitaire,
            stock=model.stock,
            agence_id=model.agence_id  # <-- ajout
        )

    @staticmethod
    def to_model(entity: PieceDetachee) -> PieceDetacheeModel:
        """
        Construit un modèle Django à partir de l'entité domaine.
        """
        return PieceDetacheeModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            prix_unitaire=entity.prix_unitaire,
            stock=entity.stock,
            agence_id=entity.agence_id
        )