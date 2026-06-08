"""
Value Object représentant une adresse email métier.
Garantit une validation stricte dès la construction.
"""

import re
from dataclasses import dataclass
from enum import Enum


class EmailValidationError(Enum):
    """Enum des erreurs possibles pour Email."""
    EMPTY_EMAIL = "L'adresse email ne peut pas être vide."
    INVALID_FORMAT = "Le format de l'adresse email est invalide."


@dataclass(frozen=True)
class Email:
    """Value Object immuable représentant un email valide."""
    value: str

    def __post_init__(self) -> None:
        """Validation appelée après l'initialisation."""
        if not self.value or not self.value.strip():
            raise ValueError(EmailValidationError.EMPTY_EMAIL.value)
        if not self._is_valid_format(self.value):
            raise ValueError(EmailValidationError.INVALID_FORMAT.value)

    @staticmethod
    def _is_valid_format(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        return self.value