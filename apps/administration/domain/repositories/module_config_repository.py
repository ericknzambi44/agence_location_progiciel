from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule


class ModuleConfigRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[ModuleConfig]:
        pass

    @abstractmethod
    def get_by_code(self, code: CodeModule) -> Optional[ModuleConfig]:
        pass

    @abstractmethod
    def add(self, config: ModuleConfig) -> None:
        pass

    @abstractmethod
    def update(self, config: ModuleConfig) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[ModuleConfig]:
        pass

    @abstractmethod
    def list_actifs(self) -> List[ModuleConfig]:
        pass