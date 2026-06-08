from dataclasses import dataclass
from enum import Enum

class ReferenceValidationError(Enum):
    VIDE = "La référence ne peut pas être vide."
    TROP_COURTE = "La référence doit comporter au moins 3 caractères."
    TROP_LONGUE = "La référence ne peut pas dépasser 50 caractères."
    FORMAT_INVALIDE = "La référence ne peut contenir que des lettres majuscules, chiffres, tirets et underscores."

@dataclass(frozen=True)
class ReferenceBien:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError(ReferenceValidationError.VIDE.value)
        val = self.value.strip().upper()
        object.__setattr__(self, 'value', val)
        if len(val) < 3:
            raise ValueError(ReferenceValidationError.TROP_COURTE.value)
        if len(val) > 50:
            raise ValueError(ReferenceValidationError.TROP_LONGUE.value)
        if not self._is_valid_format(val):
            raise ValueError(ReferenceValidationError.FORMAT_INVALIDE.value)

    @staticmethod
    def _is_valid_format(val: str) -> bool:
        import re
        return bool(re.match(r'^[A-Z0-9\-_]+$', val))