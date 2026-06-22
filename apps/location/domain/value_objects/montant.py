"""
Value Object représentant un montant en euros.
Validation : positif, avec deux décimales.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class MontantValidationError(Enum):
    NEGATIF = "Le montant ne peut pas être négatif."
    TROP_GRAND = "Le montant dépasse la limite autorisée."


@dataclass(frozen=True)
class Montant:
    valeur: Decimal

    def __post_init__(self):
        if self.valeur < 0:
            raise ValueError(MontantValidationError.NEGATIF.value)
        if self.valeur > Decimal('1e12'):
            raise ValueError(MontantValidationError.TROP_GRAND.value)