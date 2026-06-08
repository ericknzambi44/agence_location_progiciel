from uuid import UUID
from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.repositories.role_repository import RoleRepository

class AffecterRoleUseCase:
    def __init__(self, employe_repo: EmployeRepository, role_repo: RoleRepository):
        self.employe_repo = employe_repo
        self.role_repo = role_repo

    def execute(self, employe_id: UUID, role_id: UUID) -> None:
        employe = self.employe_repo.get(employe_id)
        if not employe:
            raise ValueError("Employé inexistant")
        role = self.role_repo.get(role_id)
        if not role:
            raise ValueError("Rôle inexistant")
        employe.role_id = role.id
        self.employe_repo.update(employe)