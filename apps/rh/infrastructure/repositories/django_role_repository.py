from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from rh.domain.repositories.role_repository import RoleRepository
from rh.domain.entities.role import Role
from rh.infrastructure.models import RoleModel
from rh.infrastructure.mappers.role_mapper import RoleMapper

class DjangoRoleRepository(RoleRepository):
    def get(self, id: UUID) -> Optional[Role]:
        try:
            model = RoleModel.objects.get(id=id)
            return RoleMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_nom(self, nom: str) -> Optional[Role]:
        try:
            model = RoleModel.objects.get(nom=nom)
            return RoleMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, role: Role) -> None:
        model = RoleMapper.to_model(role)
        model.save()
        role.id = model.id

    def update(self, role: Role) -> None:
        model = RoleMapper.to_model(role)
        model.save()

    def list_all(self) -> List[Role]:
        models = RoleModel.objects.all()
        return [RoleMapper.to_domain(m) for m in models]