from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from rh.domain.entities.role import Role

class RoleRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Role]:
        """Récupère un rôle par son identifiant."""
        pass

    @abstractmethod
    def get_by_nom(self, nom: str) -> Optional[Role]:
        """Récupère un rôle par son nom (unique)."""
        pass

    @abstractmethod
    def add(self, role: Role) -> None:
        """Ajoute un nouveau rôle."""
        pass

    @abstractmethod
    def update(self, role: Role) -> None:
        """Met à jour un rôle existant."""
        pass

    @abstractmethod
    def list_all(self) -> List[Role]:
        """Liste tous les rôles."""
        pass