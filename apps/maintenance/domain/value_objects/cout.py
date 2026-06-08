from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class CoutValidationError(Enum):
    NEGATIF = "Le coût ne peut pas être négatif."
    TROP_ELEVE = "Le coût dépasse 10 millions."

@dataclass(frozen=True)
class Cout:
    montant: Decimal

    def __post_init__(self):
        if self.montant < 0:
            raise ValueError(CoutValidationError.NEGATIF.value)
        if self.montant > Decimal('10_000_000'):
            raise ValueError(CoutValidationError.TROP_ELEVE.value)

    def __add__(self, other: 'Cout') -> 'Cout':
        return Cout(self.montant + other.montant)

    def __str__(self):
        return f"{self.montant:.2f} $"