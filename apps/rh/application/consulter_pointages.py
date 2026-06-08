from datetime import date
from typing import List
from uuid import UUID
from rh.domain.entities.pointage import Pointage
from rh.domain.repositories.pointage_repository import PointageRepository
from rh.domain.repositories.employe_repository import EmployeRepository

class ConsulterPointagesUseCase:
    def __init__(self, pointage_repo: PointageRepository, employe_repo: EmployeRepository):
        self.pointage_repo = pointage_repo
        self.employe_repo = employe_repo

    def execute(self, employe_id: UUID, jour: date) -> List[Pointage]:
        employe = self.employe_repo.get(employe_id)
        if not employe:
            raise ValueError("Employé inexistant")
        return self.pointage_repo.get_by_employe_and_date(employe_id, jour)