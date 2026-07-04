"""
Repository abstrait pour l'entité Client.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from location.domain.entities.client import Client
from shared_kernel.domain.value_objects import Email


class ClientRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Client]:
        pass

    @abstractmethod
    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Client]:
        pass

    @abstractmethod
    def add(self, client: Client) -> None:
        pass

    @abstractmethod
    def update(self, client: Client) -> None:
        pass

    @abstractmethod
    def list_all(self, agence_id: UUID = None) -> List[Client]:
        pass