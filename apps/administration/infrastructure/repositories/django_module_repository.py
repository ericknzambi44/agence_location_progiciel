from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from administration.domain.repositories.module_config_repository import ModuleConfigRepository
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule
from administration.infrastructure.models import ModuleConfigModel
from administration.infrastructure.mappers.module_config_mapper import ModuleConfigMapper

class DjangoModuleConfigRepository(ModuleConfigRepository):
    def get(self, id: UUID) -> Optional[ModuleConfig]:
        try:
            model = ModuleConfigModel.objects.get(id=id)
            return ModuleConfigMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_code(self, code: CodeModule) -> Optional[ModuleConfig]:
        try:
            model = ModuleConfigModel.objects.get(code=code.value)
            return ModuleConfigMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, config: ModuleConfig) -> None:
        model = ModuleConfigMapper.to_model(config)
        model.save()
        config.id = model.id

    def update(self, config: ModuleConfig) -> None:
        model = ModuleConfigMapper.to_model(config)
        obj, created = ModuleConfigModel.objects.update_or_create(
            id=model.id,
            defaults={
                'code': model.code,
                'nom': model.nom,
                'description': model.description,
                'active': model.active,
                'ordre_affichage': model.ordre_affichage,
                'parametres': model.parametres,
            }
        )
        if created:
            config.id = obj.id

    def list_all(self) -> List[ModuleConfig]:
        models = ModuleConfigModel.objects.all().order_by('ordre_affichage')
        return [ModuleConfigMapper.to_domain(m) for m in models]

    def list_actifs(self) -> List[ModuleConfig]:
        models = ModuleConfigModel.objects.filter(active=True).order_by('ordre_affichage')
        return [ModuleConfigMapper.to_domain(m) for m in models]