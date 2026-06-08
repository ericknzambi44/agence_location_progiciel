from stock.domain.entities.categorie import Categorie
from stock.infrastructure.models import CategorieModel

class CategorieMapper:
    @staticmethod
    def to_domain(model: CategorieModel) -> Categorie:
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
        parent_model = None
        if entity.parent:
            parent_model = CategorieMapper.to_model(entity.parent)
        return CategorieModel(
            id=entity.id,
            nom=entity.nom,
            description=entity.description,
            parent=parent_model
        )