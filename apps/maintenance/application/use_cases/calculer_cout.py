from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.value_objects.cout import Cout

class CalculerCoutInterventionUseCase:
    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID) -> Cout:
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        return intervention.calculer_cout()