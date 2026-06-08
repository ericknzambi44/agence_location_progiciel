from dataclasses import dataclass
from enum import Enum

class MatriculeValidationError(Enum):
    VIDE = "Le matricule ne peut pas être vide."
    FORMAT_INVALIDE = "Le matricule doit être composé de lettres majuscules et chiffres, 5 à 10 caractères."

@dataclass(frozen=True)
class Matricule:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError(MatriculeValidationError.VIDE.value)
        val = self.value.strip().upper()
        object.__setattr__(self, 'value', val)
        import re
        if not re.match(r'^[A-Z0-9]{5,10}$', val):
            raise ValueError(MatriculeValidationError.FORMAT_INVALIDE.value)