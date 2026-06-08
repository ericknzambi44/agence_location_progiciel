from dataclasses import dataclass
from enum import Enum

class DureeValidationError(Enum):
    NEGATIVE = "La durée ne peut pas être négative."
    TROP_GRANDE = "La durée dépasse 1000 heures."

@dataclass(frozen=True)
class Duree:
    heures: float  # en heures, peut être fractionnaire (ex: 0.5 pour 30 min)

    def __post_init__(self):
        if self.heures < 0:
            raise ValueError(DureeValidationError.NEGATIVE.value)
        if self.heures > 1000:
            raise ValueError(DureeValidationError.TROP_GRANDE.value)

    def __str__(self):
        return f"{self.heures}h"