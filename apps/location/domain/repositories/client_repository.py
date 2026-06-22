from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from location.domain.entities.client import Client
from shared_kernel.domain.value_objects import Email


class ClientRepository(ABC):
    @abstractmethod
    def get(self, id: UUID) -> Optional[Client]: ...
    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[Client]: ...
    @abstractmethod
    def add(self, client: Client) -> None: ...
    @abstractmethod
    def update(self, client: Client) -> None: ...
    @abstractmethod
    def list_all(self) -> List[Client]: ...