from datetime import date
from uuid import UUID
from rh.domain.entities.evaluation import Evaluation
from rh.domain.value_objects.note import Note
from rh.domain.repositories.evaluation_repository import EvaluationRepository
from rh.domain.repositories.employe_repository import EmployeRepository

class CreerEvaluationUseCase:
    def __init__(self, eval_repo: EvaluationRepository, employe_repo: EmployeRepository):
        self.eval_repo = eval_repo
        self.employe_repo = employe_repo

    def execute(self, employe_id: UUID, note_valeur: float, commentaires: str, evaluateur_id: UUID = None) -> Evaluation:
        employe = self.employe_repo.get(employe_id)
        if not employe:
            raise ValueError("Employé inexistant")
        note = Note(note_valeur)
        # Vérifier délai entre évaluations (ex: 6 mois)
        dernieres = self.eval_repo.get_last_for_employe(employe_id)  # à implémenter
        if dernieres and (date.today() - dernieres[0].date_evaluation).days < 180:
            raise ValueError("Une évaluation a eu lieu il y a moins de 6 mois")

        evaluation = Evaluation(
            employe_id=employe_id,
            date_evaluation=date.today(),
            note=note,
            commentaires=commentaires,
            evaluateur_id=evaluateur_id
        )
        self.eval_repo.add(evaluation)
        return evaluation