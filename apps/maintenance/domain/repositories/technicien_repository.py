from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.technicien import Technicien

class TechnicienRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Technicien]:
        pass

    @abstractmethod
    def add(self, technicien: Technicien) -> None:
        pass

    @abstractmethod
    def update(self, technicien: Technicien) -> None:
        """Met à jour un technicien existant."""
        pass

    @abstractmethod
    def remove(self, technicien: Technicien) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Technicien]:
        pass