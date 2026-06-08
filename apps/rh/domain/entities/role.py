from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Set

@dataclass
class Permission:
    code: str          # ex: "view_employe", "edit_pointage"
    description: str

@dataclass
class Role:
    id: UUID = field(default_factory=uuid4)
    nom: str
    permissions: Set[Permission] = field(default_factory=set)

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du rôle est obligatoire")

    def ajouter_permission(self, permission: Permission):
        self.permissions.add(permission)

    def retirer_permission(self, permission: Permission):
        self.permissions.discard(permission)

    def a_permission(self, code: str) -> bool:
        return any(p.code == code for p in self.permissions)