from uuid import UUID
from administration.domain.repositories.module_config_repository import ModuleConfigRepository

class DesactiverModuleUseCase:
    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self, module_id: UUID) -> None:
        module = self.repo.get(module_id)
        if not module:
            raise ValueError("Module non trouvé")
        module.desactiver()
        self.repo.update(module)