"""
Port (interface) du repository des mouvements de stock.
"""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class MouvementStockRepository(ABC):
    """
    Interface pour l'historique des mouvements de stock.
    """

    @abstractmethod
    def add(self, mouvement) -> None:
        """
        Enregistre un nouveau mouvement.
        """
        pass

    @abstractmethod
    def get_all(self, agence_id: UUID = None) -> List:
        """
        Retourne tous les mouvements de stock, filtrés par agence.
        """
        pass