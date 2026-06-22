"""
Value Object représentant une durée en jours.
"""
from dataclasses import dataclass
from enum import Enum


class DureeValidationError(Enum):
    NEGATIVE = "La durée ne peut pas être négative."
    NULLE = "La durée doit être supérieure à 0."


@dataclass(frozen=True)
class Duree:
    jours: int

    def __post_init__(self):
        if self.jours <= 0:
            raise ValueError(DureeValidationError.NULLE.value)