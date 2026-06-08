from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.technicien import Technicien

class TechnicienRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Technicien]:
        pass

    @abstractmethod
    def get_all(self) -> List[Technicien]:
        pass