from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from location.domain.entities.regle_tarification import ReglesTarification


class RegleTarificationRepository(ABC):
    @abstractmethod
    def get(self, agence_id: UUID) -> Optional[ReglesTarification]:
        """Récupère les règles pour une agence."""
        pass

    @abstractmethod
    def save(self, regles: ReglesTarification) -> None:
        """Sauvegarde (écrase) les règles pour une agence."""
        pass