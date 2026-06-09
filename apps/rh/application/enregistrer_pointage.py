from datetime import datetime
from uuid import UUID
from rh.domain.entities.pointage import Pointage, TypePointage
from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.repositories.pointage_repository import PointageRepository
from rh.domain.enums.error_codes import PointageError

class EnregistrerPointageUseCase:
    def __init__(self, employe_repo: EmployeRepository, pointage_repo: PointageRepository):
        self.employe_repo = employe_repo
        self.pointage_repo = pointage_repo

    def execute(self, employe_id: UUID, type_str: str, horodatage: datetime = None) -> Pointage:
        employe = self.employe_repo.get(employe_id)
        if not employe:
            raise ValueError("Employé inexistant")
        if not employe.est_actif:
            raise ValueError("Employé inactif")

        if horodatage is None:
            horodatage = datetime.now()

        # Vérifier les règles de cohérence (ex: ne pas avoir deux entrées sans sortie)
        dernier = self.pointage_repo.get_dernier_pointage(employe_id)
        if type_str == TypePointage.ENTRY and dernier and dernier.type == TypePointage.ENTRY:
            raise ValueError(PointageError.DOUBLON_ENTREE.value)
        if type_str == TypePointage.EXIT and (not dernier or dernier.type == TypePointage.EXIT):
            raise ValueError(PointageError.SORTIE_SANS_ENTREE.value)

        pointage = Pointage(
            employe_id=employe_id,
            horodatage=horodatage,
            type=type_str
        )
        self.pointage_repo.add(pointage)
        return pointage