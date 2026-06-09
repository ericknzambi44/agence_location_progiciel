from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule
from administration.infrastructure.models import ModuleConfigModel

class ModuleConfigMapper:
    @staticmethod
    def to_domain(model: ModuleConfigModel) -> ModuleConfig:
        code = CodeModule(model.code)
        return ModuleConfig(
            id=model.id,
            code=code,
            nom=model.nom,
            description=model.description or "",
            active=model.active,
            ordre_affichage=model.ordre_affichage,
            parametres=model.parametres or {}
        )

    @staticmethod
    def to_model(entity: ModuleConfig) -> ModuleConfigModel:
        return ModuleConfigModel(
            id=entity.id,
            code=entity.code.value,
            nom=entity.nom,
            description=entity.description,
            active=entity.active,
            ordre_affichage=entity.ordre_affichage,
            parametres=entity.parametres
        )