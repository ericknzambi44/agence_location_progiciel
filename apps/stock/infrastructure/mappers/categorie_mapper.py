"""
Mapper pour convertir entre l'entité domaine Categorie et le modèle Django Categorie.
"""

from stock.domain.entities.categorie import Categorie
from stock.infrastructure.models import Categorie as CategorieModel  # alias pour cohérence


class CategorieMapper:
    """
    Conversion bidirectionnelle entre l'entité Categorie et le modèle ORM.
    """

    @staticmethod
    def to_domain(model: CategorieModel) -> Categorie:
        """
        Construit une entité Categorie à partir du modèle Django.

        Args:
            model (CategorieModel): Instance du modèle ORM.

        Returns:
            Categorie: Entité domaine.
        """
        parent = None
        if model.parent:
            parent = CategorieMapper.to_domain(model.parent)
        return Categorie(
            id=model.id,
            nom=model.nom,
            description=model.description,
            parent=parent
        )

    @staticmethod
    def to_model(entity: Categorie) -> CategorieModel:
        """
        Construit un modèle Django à partir de l'entité Categorie.

        Args:
            entity (Categorie): Entité domaine.

        Returns:
            CategorieModel: Instance du modèle ORM.
        """
        parent_model = None
        if entity.parent:
            parent_model = CategorieMapper.to_model(entity.parent)
        return CategorieModel(
            id=entity.id,
            nom=entity.nom,
            description=entity.description,
            parent=parent_model
        )