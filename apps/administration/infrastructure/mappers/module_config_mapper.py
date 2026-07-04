"""
Mapper entre l'entité domaine ModuleConfig et le modèle ORM ModuleConfigModel.
Assure la conversion dans les deux sens, incluant l'agence_id pour le multi-agences.
"""
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule
from administration.infrastructure.models import ModuleConfigModel


class ModuleConfigMapper:
    """Conversion bidirectionnelle pour les configurations de modules."""

    @staticmethod
    def to_domain(model: ModuleConfigModel) -> ModuleConfig:
        """
        Construit une entité ModuleConfig à partir du modèle Django.
        """
        code = CodeModule(model.code)
        return ModuleConfig(
            id=model.id,
            code=code,
            nom=model.nom,
            description=model.description or "",
            active=model.active,
            ordre_affichage=model.ordre_affichage,
            parametres=model.parametres or {},
            agence_id=model.agence_id  # <-- ajout de l'agence_id
        )

    @staticmethod
    def to_model(entity: ModuleConfig) -> ModuleConfigModel:
        """
        Construit un modèle Django à partir de l'entité ModuleConfig.
        """
        return ModuleConfigModel(
            id=entity.id,
            code=entity.code.value,
            nom=entity.nom,
            description=entity.description,
            active=entity.active,
            ordre_affichage=entity.ordre_affichage,
            parametres=entity.parametres,
            agence_id=entity.agence_id  
        )