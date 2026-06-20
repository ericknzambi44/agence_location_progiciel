"""
Repository abstrait pour les pièces détachées.
Définit le contrat que doivent respecter les implémentations concrètes.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.piece_detachee import PieceDetachee


class PieceDetacheeRepository(ABC):
    """Interface pour la persistance des pièces détachées."""

    @abstractmethod
    def get(self, id: UUID) -> Optional[PieceDetachee]:
        """Récupère une pièce par son identifiant UUID."""
        pass

    @abstractmethod
    def add(self, piece: PieceDetachee) -> None:
        """Ajoute une nouvelle pièce en base."""
        pass

    @abstractmethod
    def update(self, piece: PieceDetachee) -> None:
        """Met à jour une pièce existante."""
        pass

    @abstractmethod
    def remove(self, piece: PieceDetachee) -> None:
        """Supprime une pièce de la base."""
        pass

    @abstractmethod
    def find_by_reference(self, reference: str) -> Optional[PieceDetachee]:
        """Recherche une pièce par sa référence unique."""
        pass

    @abstractmethod
    def find_all(self) -> List[PieceDetachee]:
        """Retourne toutes les pièces détachées."""
        pass