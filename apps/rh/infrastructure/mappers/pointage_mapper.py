from rh.domain.entities.pointage import Pointage
from rh.infrastructure.models import PointageModel

class PointageMapper:
    @staticmethod
    def to_domain(model: PointageModel) -> Pointage:
        return Pointage(
            id=model.id,
            employe_id=model.employe_id,
            horodatage=model.horodatage,
            type=model.type,
            commentaire=model.commentaire or ""
        )

    @staticmethod
    def to_model(entity: Pointage) -> PointageModel:
        return PointageModel(
            id=entity.id,
            employe_id=entity.employe_id,
            horodatage=entity.horodatage,
            type=entity.type,
            commentaire=entity.commentaire
        )