from abc import ABC, abstractmethod
from typing import List
from datetime import date
from uuid import UUID
from stock.domain.entities.disponibilite import DisponibilitePeriode
from stock.domain.entities.bien import Bien

class DisponibiliteRepository(ABC):
    @abstractmethod
    def add(self, periode: DisponibilitePeriode) -> None: ...
    @abstractmethod
    def find_by_bien_et_periode(self, bien_id: UUID, debut: date, fin: date) -> List[DisponibilitePeriode]: ...
    @abstractmethod
    def clear_conflicts(self, bien_id: UUID, debut: date, fin: date) -> None: ...