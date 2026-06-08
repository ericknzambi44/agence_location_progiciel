from dataclasses import dataclass
from enum import Enum

class QuantiteValidationError(Enum):
    NEGATIVE = "La quantité ne peut pas être négative."
    TROP_GRANDE = "La quantité dépasse la limite (1e8)."

@dataclass(frozen=True)
class Quantite:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(QuantiteValidationError.NEGATIVE.value)
        if self.value > 100_000_000:
            raise ValueError(QuantiteValidationError.TROP_GRANDE.value)