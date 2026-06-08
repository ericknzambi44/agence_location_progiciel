from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from rh.domain.entities.employe import Employe
from rh.domain.value_objects.matricule import Matricule
from shared_kernel.domain.value_objects import Email

class EmployeRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Employe]: ...
    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[Employe]: ...
    @abstractmethod
    def get_by_matricule(self, matricule: Matricule) -> Optional[Employe]: ...
    @abstractmethod
    def add(self, employe: Employe) -> None: ...
    @abstractmethod
    def update(self, employe: Employe) -> None: ...
    @abstractmethod
    def list_actifs(self) -> List[Employe]: ...