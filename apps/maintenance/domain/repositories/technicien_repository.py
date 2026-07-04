"""
Repository abstrait pour les techniciens.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.technicien import Technicien


class TechnicienRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Technicien]:
        pass

    @abstractmethod
    def add(self, technicien: Technicien) -> None:
        pass

    @abstractmethod
    def update(self, technicien: Technicien) -> None:
        pass

    @abstractmethod
    def remove(self, technicien: Technicien) -> None:
        pass

    @abstractmethod
    def get_all(self, agence_id: UUID = None) -> List[Technicien]:
        pass