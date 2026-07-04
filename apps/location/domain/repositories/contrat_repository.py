"""
Repository abstrait pour l'entité Contrat.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import date
from location.domain.entities.contrat import Contrat


class ContratRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Contrat]:
        pass

    @abstractmethod
    def add(self, contrat: Contrat) -> None:
        pass

    @abstractmethod
    def update(self, contrat: Contrat) -> None:
        pass

    @abstractmethod
    def find_by_bien_et_periode(self, bien_id: UUID, debut: date, fin: date, agence_id: UUID = None) -> List[Contrat]:
        """Retourne les contrats actifs qui chevauchent la période pour un bien donné."""
        pass

    @abstractmethod
    def find_by_client(self, client_id: UUID, agence_id: UUID = None) -> List[Contrat]:
        pass

    @abstractmethod
    def find_actifs(self, agence_id: UUID = None) -> List[Contrat]:
        pass