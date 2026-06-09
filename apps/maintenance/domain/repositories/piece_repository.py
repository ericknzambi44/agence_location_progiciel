from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.piece_detachee import PieceDetachee

class PieceDetacheeRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[PieceDetachee]:
        pass

    @abstractmethod
    def add(self, piece: PieceDetachee) -> None:
        pass

    @abstractmethod
    def update(self, piece: PieceDetachee) -> None:
        """Met à jour une pièce détachée existante."""
        pass

    @abstractmethod
    def remove(self, piece: PieceDetachee) -> None:
        pass

    @abstractmethod
    def find_by_reference(self, reference: str) -> Optional[PieceDetachee]:
        pass

    @abstractmethod
    def find_all(self) -> List[PieceDetachee]:
        pass