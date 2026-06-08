from rh.domain.entities.role import Role, Permission
from rh.infrastructure.models import RoleModel

class RoleMapper:
    @staticmethod
    def to_domain(model: RoleModel) -> Role:
        permissions = {Permission(p['code'], p['description']) for p in model.permissions}
        return Role(
            id=model.id,
            nom=model.nom,
            permissions=permissions
        )

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        permissions_list = [{"code": p.code, "description": p.description} for p in entity.permissions]
        return RoleModel(
            id=entity.id,
            nom=entity.nom,
            permissions=permissions_list
        )