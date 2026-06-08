from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from stock.domain.entities.mouvement_stock import MouvementStock
from stock.domain.entities.bien import Bien

class MouvementStockRepository(ABC):
    @abstractmethod
    def add(self, mouvement: MouvementStock) -> None: ...
    @abstractmethod
    def get_by_bien(self, bien_id: UUID) -> List[MouvementStock]: ...
    @abstractmethod
    def get_solde_bien(self, bien_id: UUID) -> int: ...  # calcule stock net