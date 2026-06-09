from dataclasses import dataclass
from enum import Enum

class CodeModuleValidationError(Enum):
    VIDE = "Le code module ne peut pas être vide."
    FORMAT_INVALIDE = "Le code module doit contenir 3 à 20 caractères alphanumériques (sans espace)."

@dataclass(frozen=True)
class CodeModule:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError(CodeModuleValidationError.VIDE.value)
        val = self.value.strip().lower()
        object.__setattr__(self, 'value', val)
        import re
        if not re.match(r'^[a-z0-9_]{3,20}$', val):
            raise ValueError(CodeModuleValidationError.FORMAT_INVALIDE.value)