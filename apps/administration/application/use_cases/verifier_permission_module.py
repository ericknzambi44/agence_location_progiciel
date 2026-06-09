from uuid import UUID
from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.repositories.role_repository import RoleRepository

class VerifierPermissionUseCase:
    def __init__(self, employe_repo: EmployeRepository, role_repo: RoleRepository):
        self.employe_repo = employe_repo
        self.role_repo = role_repo

    def execute(self, employe_id: UUID, permission_code: str) -> bool:
        employe = self.employe_repo.get(employe_id)
        if not employe or not employe.est_actif:
            return False
        if not employe.role_id:
            return False
        role = self.role_repo.get(employe.role_id)
        if not role:
            return False
        return role.a_permission(permission_code)