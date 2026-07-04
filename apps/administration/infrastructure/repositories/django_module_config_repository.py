"""
Repository Django pour la configuration des modules.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from administration.domain.repositories.module_config_repository import ModuleConfigRepository
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule
from administration.infrastructure.models import ModuleConfigModel
from administration.infrastructure.mappers.module_config_mapper import ModuleConfigMapper


class DjangoModuleConfigRepository(ModuleConfigRepository):
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[ModuleConfig]:
        try:
            qs = ModuleConfigModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ModuleConfigMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_code(self, code: CodeModule, agence_id: UUID = None) -> Optional[ModuleConfig]:
        try:
            qs = ModuleConfigModel.objects.filter(code=code.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ModuleConfigMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, config: ModuleConfig) -> None:
        if config.agence_id is None:
            raise ValueError("agence_id est requis pour créer une configuration de module.")
        model = ModuleConfigMapper.to_model(config)
        model.save()
        config.id = model.id

    def update(self, config: ModuleConfig) -> None:
        model = ModuleConfigMapper.to_model(config)
        # On met à jour en s'assurant que l'agence_id ne change pas (on pourrait le laisser)
        obj, created = ModuleConfigModel.objects.update_or_create(
            id=model.id,
            defaults={
                'code': model.code,
                'nom': model.nom,
                'description': model.description,
                'active': model.active,
                'ordre_affichage': model.ordre_affichage,
                'parametres': model.parametres,
                'agence_id': model.agence_id  # on préserve l'agence
            }
        )
        if created:
            config.id = obj.id

    def list_all(self, agence_id: UUID = None) -> List[ModuleConfig]:
        if agence_id is None:
            return []  # sécurité, sauf si superuser (géré dans le viewset)
        models = ModuleConfigModel.objects.filter(agence_id=agence_id).order_by('ordre_affichage')
        return [ModuleConfigMapper.to_domain(m) for m in models]

    def list_actifs(self, agence_id: UUID = None) -> List[ModuleConfig]:
        if agence_id is None:
            return []
        models = ModuleConfigModel.objects.filter(active=True, agence_id=agence_id).order_by('ordre_affichage')
        return [ModuleConfigMapper.to_domain(m) for m in models]