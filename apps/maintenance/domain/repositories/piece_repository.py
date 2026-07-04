"""
Repository abstrait pour les pièces détachées.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.piece_detachee import PieceDetachee


class PieceDetacheeRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[PieceDetachee]:
        pass

    @abstractmethod
    def add(self, piece: PieceDetachee) -> None:
        pass

    @abstractmethod
    def update(self, piece: PieceDetachee) -> None:
        pass

    @abstractmethod
    def remove(self, piece: PieceDetachee) -> None:
        pass

    @abstractmethod
    def find_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[PieceDetachee]:
        pass

    @abstractmethod
    def find_all(self, agence_id: UUID = None) -> List[PieceDetachee]:
        pass