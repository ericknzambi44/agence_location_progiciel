from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from maintenance.domain.entities.intervention import Intervention

class InterventionRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Intervention]:
        pass

    @abstractmethod
    def add(self, intervention: Intervention) -> None:
        pass

    @abstractmethod
    def update(self, intervention: Intervention) -> None:
        """Met à jour une intervention existante."""
        pass

    @abstractmethod
    def remove(self, intervention: Intervention) -> None:
        pass

    @abstractmethod
    def find_by_bien(self, bien_id: UUID) -> List[Intervention]:
        pass

    @abstractmethod
    def find_by_technicien(self, technicien_id: UUID) -> List[Intervention]:
        pass

    @abstractmethod
    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime) -> List[Intervention]:
        """Retourne les interventions du technicien qui chevauchent la période."""
        pass

    @abstractmethod
    def find_all(self) -> List[Intervention]:
        pass