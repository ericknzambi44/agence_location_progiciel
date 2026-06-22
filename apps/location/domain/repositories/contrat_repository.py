from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import date
from location.domain.entities.contrat import Contrat


class ContratRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Contrat]: ...
    @abstractmethod
    def add(self, contrat: Contrat) -> None: ...
    @abstractmethod
    def update(self, contrat: Contrat) -> None: ...
    @abstractmethod
    def find_by_bien_et_periode(self, bien_id: UUID, debut: date, fin: date) -> List[Contrat]:
        """Retourne les contrats actifs qui chevauchent la période donnée pour un bien."""
        pass
    @abstractmethod
    def find_by_client(self, client_id: UUID) -> List[Contrat]: ...
    @abstractmethod
    def find_actifs(self) -> List[Contrat]: ...