"""
Mapper Evaluation : convertit entre le modèle Django `Evaluation` et l'entité domaine `Evaluation`.

Fait partie de la couche infrastructure (persistance).
"""

from rh.domain.entities.evaluation import Evaluation
from rh.domain.value_objects.note import Note
from rh.infrastructure.models import Evaluation as EvaluationModel  # alias


class EvaluationMapper:
    """
    Convertit les objets entre le modèle de persistance `Evaluation`
    et l'entité du domaine `Evaluation`.
    """

    @staticmethod
    def to_domain(model: EvaluationModel) -> Evaluation:
        """
        Convertit une instance `EvaluationModel` en entité domaine.

        Args:
            model (EvaluationModel): Instance du modèle ORM.

        Returns:
            Evaluation: Entité domaine correspondante.
        """
        return Evaluation(
            id=model.id,
            employe_id=model.employe_id,
            date_evaluation=model.date_evaluation,
            note=Note(model.note),
            commentaires=model.commentaires or "",
            evaluateur_id=model.evaluateur_id,
        )

    @staticmethod
    def to_model(entity: Evaluation) -> EvaluationModel:
        """
        Convertit une entité domaine `Evaluation` en instance du modèle Django.

        Args:
            entity (Evaluation): Entité domaine à convertir.

        Returns:
            EvaluationModel: Instance du modèle ORM (non persistée).
        """
        return EvaluationModel(
            id=entity.id,
            employe_id=entity.employe_id,
            date_evaluation=entity.date_evaluation,
            note=entity.note.valeur,
            commentaires=entity.commentaires,
            evaluateur_id=entity.evaluateur_id,
        )