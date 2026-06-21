from dataclasses import dataclass
from enum import Enum


class CodeAgenceValidationError(Enum):
    VIDE = "Le code agence ne peut pas être vide."
    FORMAT_INVALIDE = "Le code doit contenir des lettres majuscules et des chiffres, 3 à 10 caractères."


@dataclass(frozen=True)
class CodeAgence:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError(CodeAgenceValidationError.VIDE.value)
        val = self.value.strip().upper()
        object.__setattr__(self, 'value', val)
        import re
        if not re.match(r'^[A-Z0-9]{3,10}$', val):
            raise ValueError(CodeAgenceValidationError.FORMAT_INVALIDE.value)