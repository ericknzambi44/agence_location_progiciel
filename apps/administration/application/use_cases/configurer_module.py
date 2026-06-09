from uuid import UUID
from typing import Any
from administration.domain.repositories.module_config_repository import ModuleConfigRepository

class ConfigurerModuleUseCase:
    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self, module_id: UUID, parametres: dict[str, Any]) -> None:
        module = self.repo.get(module_id)
        if not module:
            raise ValueError("Module non trouvé")
        for cle, valeur in parametres.items():
            module.definir_parametre(cle, valeur)
        self.repo.update(module)