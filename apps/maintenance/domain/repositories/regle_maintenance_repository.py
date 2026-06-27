"""
Repository abstrait pour la persistance des règles de tarification de maintenance.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from maintenance.domain.entities.regle_maintenance import ReglesMaintenance


class RegleMaintenanceRepository(ABC):
    """
    Interface pour l'accès aux règles de tarification de maintenance.
    """

    @abstractmethod
    def get(self, agence_id: UUID) -> Optional[ReglesMaintenance]:
        """
        Récupère l'ensemble des règles de tarification pour une agence.
        Retourne None si aucune règle n'est définie.
        """
        pass

    @abstractmethod
    def save(self, regles: ReglesMaintenance) -> None:
        """
        Sauvegarde (remplace) l'ensemble des règles pour une agence.
        """
        pass