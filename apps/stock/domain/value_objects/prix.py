from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

class PrixValidationError(Enum):
    NEGATIF = "Le prix ne peut pas être négatif."
    TROP_GRAND = "Le prix dépasse la limite autorisée (1e12)."

@dataclass(frozen=True)
class PrixHT:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(PrixValidationError.NEGATIF.value)
        if self.amount > Decimal('1e12'):
            raise ValueError(PrixValidationError.TROP_GRAND.value)
        # On pourrait valider la devise plus tard