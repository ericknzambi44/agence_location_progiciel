from dataclasses import dataclass
from enum import Enum

class NoteValidationError(Enum):
    HORS_BORNE = "La note doit être comprise entre 0 et 10."

@dataclass(frozen=True)
class Note:
    valeur: float

    def __post_init__(self):
        if not (0 <= self.valeur <= 10):
            raise ValueError(NoteValidationError.HORS_BORNE.value)