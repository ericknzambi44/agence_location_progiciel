"""
Repository abstrait pour les interventions de maintenance.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from maintenance.domain.entities.intervention import Intervention


class InterventionRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Intervention]:
        pass

    @abstractmethod
    def add(self, intervention: Intervention) -> None:
        pass

    @abstractmethod
    def update(self, intervention: Intervention) -> None:
        pass

    @abstractmethod
    def remove(self, intervention: Intervention) -> None:
        pass

    @abstractmethod
    def find_by_bien(self, bien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        pass

    @abstractmethod
    def find_by_technicien(self, technicien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        pass

    @abstractmethod
    def find_by_periode(self, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        pass

    @abstractmethod
    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        pass

    @abstractmethod
    def find_all(self, agence_id: UUID = None) -> List[Intervention]:
        pass