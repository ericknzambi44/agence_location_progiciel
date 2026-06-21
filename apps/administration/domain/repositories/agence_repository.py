"""
Repository abstrait pour les agences.
Définit les opérations de persistance nécessaires.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from administration.domain.entities.agence import Agence
from administration.domain.value_objects.code_agence import CodeAgence


class AgenceRepository(ABC):
    """Interface pour la persistance des agences."""

    @abstractmethod
    def get(self, id: UUID) -> Optional[Agence]:
        pass

    @abstractmethod
    def get_by_code(self, code: CodeAgence) -> Optional[Agence]:
        pass

    @abstractmethod
    def get_by_nom(self, nom: str) -> Optional[Agence]:
        pass

    @abstractmethod
    def add(self, agence: Agence) -> None:
        pass

    @abstractmethod
    def update(self, agence: Agence) -> None:
        pass

    @abstractmethod
    def list_actives(self) -> List[Agence]:
        pass

    @abstractmethod
    def list_all(self) -> List[Agence]:
        pass