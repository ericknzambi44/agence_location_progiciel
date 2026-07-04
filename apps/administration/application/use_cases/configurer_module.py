from uuid import UUID
from typing import Any, Dict
from administration.domain.repositories.module_config_repository import ModuleConfigRepository


class ConfigurerModuleUseCase:
    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self, module_id: UUID, parametres: Dict[str, Any], agence_id: UUID = None) -> None:
        if agence_id is None:
            raise ValueError("agence_id est requis pour configurer un module.")
        module = self.repo.get(module_id, agence_id=agence_id)
        if not module:
            raise ValueError("Module non trouvé ou non autorisé")
        for cle, valeur in parametres.items():
            module.definir_parametre(cle, valeur)
        self.repo.update(module)