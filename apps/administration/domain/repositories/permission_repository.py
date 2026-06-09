from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from rh.domain.entities.role import Permission


class PermissionRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Permission]: ...
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Permission]: ...
    @abstractmethod
    def add(self, permission: Permission) -> None: ...
    @abstractmethod
    def list_by_module(self, module_code: str) -> List[Permission]: ...