from typing import List
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.repositories.module_config_repository import ModuleConfigRepository

class ListerModulesActifsUseCase:
    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self) -> List[ModuleConfig]:
        return self.repo.list_actifs()