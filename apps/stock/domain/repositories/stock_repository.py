"""
Port (interface) du repository de stock.

Définit les opérations de consultation et de mise à jour des niveaux de stock,
indépendamment de la technologie de persistance.
"""

from abc import ABC, abstractmethod
from uuid import UUID


class StockRepository(ABC):
    """
    Interface pour la gestion des niveaux de stock.
    """

    @abstractmethod
    def get_article(self, article_id: UUID, agence_id: UUID = None):
        """
        Récupère un article de stock par son identifiant.

        Returns:
            Article ou None si introuvable.
        """
        pass

    @abstractmethod
    def get_quantite_disponible(self, article_id: UUID, agence_id: UUID = None) -> int:
        """
        Retourne la quantité disponible pour un article donné.
        """
        pass

    @abstractmethod
    def incrementer_stock(self, article_id: UUID, quantite: int, agence_id: UUID = None) -> None:
        """
        Augmente le stock d'un article.
        """
        pass

    @abstractmethod
    def decrementer_stock(self, article_id: UUID, quantite: int, agence_id: UUID = None) -> None:
        """
        Diminue le stock d'un article.
        """
        pass