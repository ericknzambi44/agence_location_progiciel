"""
Value Object représentant une règle de tarification.
Immuable, avec validation.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum


class TypeRegle(Enum):
    FORFAIT = "forfait"
    REMISE = "remise"
    MAJORATION = "majoration"


@dataclass(frozen=True)
class RegleTarification:
    type: TypeRegle
    valeur: Decimal
    duree_min: int
    duree_max: Optional[int] = None
    type_bien_id: Optional[UUID] = None
    periode_debut: Optional[date] = None
    periode_fin: Optional[date] = None
    description: str = ""
    active: bool = True

    def __post_init__(self):
        if self.valeur < 0:
            raise ValueError("La valeur doit être positive")
        if self.type == TypeRegle.FORFAIT and self.valeur <= 0:
            raise ValueError("Un forfait doit avoir une valeur > 0")
        if self.duree_min < 0:
            raise ValueError("duree_min doit être >= 0")
        if self.duree_max is not None and self.duree_max < self.duree_min:
            raise ValueError("duree_max doit être >= duree_min")
        if self.periode_debut and self.periode_fin and self.periode_debut > self.periode_fin:
            raise ValueError("periode_debut doit être avant periode_fin")

    def est_applicable(self, duree: int, type_bien_id: UUID, date_debut: date) -> bool:
        if not self.active:
            return False
        if duree < self.duree_min:
            return False
        if self.duree_max is not None and duree > self.duree_max:
            return False
        if self.type_bien_id and self.type_bien_id != type_bien_id:
            return False
        if self.periode_debut and date_debut < self.periode_debut:
            return False
        if self.periode_fin and date_debut > self.periode_fin:
            return False
        return True