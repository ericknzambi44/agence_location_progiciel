from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository

class DemarrerInterventionUseCase:
    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID):
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        intervention.demarrer()
        self.repo.add(intervention)