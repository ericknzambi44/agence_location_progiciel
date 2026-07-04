from uuid import UUID
from administration.domain.repositories.module_config_repository import ModuleConfigRepository


class ActiverModuleUseCase:
    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self, module_id: UUID, agence_id: UUID = None) -> None:
        if agence_id is None:
            raise ValueError("agence_id est requis pour activer un module.")
        module = self.repo.get(module_id, agence_id=agence_id)
        if not module:
            raise ValueError("Module non trouvé ou non autorisé")
        module.activer()
        self.repo.update(module)