from uuid import UUID
from decimal import Decimal
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.value_objects.cout import Cout

class CalculerCoutInterventionUseCase:
    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID) -> Cout:
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        cout_total_float = intervention.calculer_cout() 
        return Cout(Decimal(str(cout_total_float)))