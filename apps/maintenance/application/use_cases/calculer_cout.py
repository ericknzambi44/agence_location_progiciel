from decimal import Decimal
from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.application.services.tarification_maintenance_service import TarificationMaintenanceService
from maintenance.domain.value_objects.cout import Cout

class CalculerCoutInterventionUseCase:
    def __init__(self, repo: InterventionRepository, tarif_service: TarificationMaintenanceService):
        self.repo = repo
        self.tarif_service = tarif_service

    def execute(self, intervention_id: UUID) -> Cout:
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        return Cout(Decimal(str(intervention.calculer_cout(self.tarif_service))))