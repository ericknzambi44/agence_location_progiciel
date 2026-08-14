"""
Mapper Role : convertit entre le modèle Django `Role` et l'entité domaine `Role`.

Fait partie de la couche infrastructure (persistance).
Le modèle Django stocke les permissions sous forme de liste JSON,
tandis que le domaine utilise un ensemble d'objets `Permission`.
"""

from rh.domain.entities.role import Role, Permission
from rh.infrastructure.models import Role as RoleModel  # alias


class RoleMapper:
    """
    Convertit les objets entre le modèle de persistance `Role`
    et l'entité du domaine `Role`.
    """

    @staticmethod
    def to_domain(model: RoleModel) -> Role:
        """
        Convertit une instance `RoleModel` en entité domaine.

        Args:
            model (RoleModel): Instance du modèle ORM.

        Returns:
            Role: Entité domaine correspondante.
        """
        permissions = {
            Permission(p['code'], p['description']) for p in model.permissions
        }
        return Role(
            id=model.id,
            nom=model.nom,
            permissions=permissions,
        )

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        """
        Convertit une entité domaine `Role` en instance du modèle Django.

        Args:
            entity (Role): Entité domaine à convertir.

        Returns:
            RoleModel: Instance du modèle ORM (non persistée).
        """
        permissions_list = [
            {"code": p.code, "description": p.description}
            for p in entity.permissions
        ]
        return RoleModel(
            id=entity.id,
            nom=entity.nom,
            permissions=permissions_list,
        )