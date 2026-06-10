from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository

class TerminerInterventionUseCase:
    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID) -> float:
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        cout_total = intervention.terminer()
        self.repo.update(intervention)
        return cout_total