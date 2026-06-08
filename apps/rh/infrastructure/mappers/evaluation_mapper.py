from rh.domain.entities.evaluation import Evaluation
from rh.domain.value_objects.note import Note
from rh.infrastructure.models import EvaluationModel

class EvaluationMapper:
    @staticmethod
    def to_domain(model: EvaluationModel) -> Evaluation:
        return Evaluation(
            id=model.id,
            employe_id=model.employe_id,
            date_evaluation=model.date_evaluation,
            note=Note(model.note),
            commentaires=model.commentaires or "",
            evaluateur_id=model.evaluateur_id
        )

    @staticmethod
    def to_model(entity: Evaluation) -> EvaluationModel:
        return EvaluationModel(
            id=entity.id,
            employe_id=entity.employe_id,
            date_evaluation=entity.date_evaluation,
            note=entity.note.valeur,
            commentaires=entity.commentaires,
            evaluateur_id=entity.evaluateur_id
        )