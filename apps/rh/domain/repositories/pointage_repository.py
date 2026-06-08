from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List
from uuid import UUID
from rh.domain.entities.pointage import Pointage

class PointageRepository(ABC):
    @abstractmethod
    def add(self, pointage: Pointage) -> None: ...
    @abstractmethod
    def get_by_employe_and_date(self, employe_id: UUID, jour: date) -> List[Pointage]: ...
    @abstractmethod
    def get_dernier_pointage(self, employe_id: UUID) -> Pointage | None: ...