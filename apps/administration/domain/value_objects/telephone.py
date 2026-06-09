from dataclasses import dataclass
from enum import Enum

class TelephoneValidationError(Enum):
    VIDE = "Le numéro de téléphone ne peut pas être vide."
    FORMAT_INVALIDE = "Le numéro doit contenir au moins 6 chiffres, espaces et tirets autorisés."

@dataclass(frozen=True)
class Telephone:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError(TelephoneValidationError.VIDE.value)
        # On nettoie en supprimant espaces/tirets pour vérifier la présence de chiffres
        cleaned = ''.join(c for c in self.value if c.isdigit())
        if len(cleaned) < 6:
            raise ValueError(TelephoneValidationError.FORMAT_INVALIDE.value)