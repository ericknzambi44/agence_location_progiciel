"""
Value Object pour les noms de personnes (prénom, nom).
Assure des règles métier : non vide, longueur minimale, caractères autorisés.
"""

from dataclasses import dataclass
from enum import Enum


class NameValidationError(Enum):
    EMPTY_NAME = "Le nom ne peut pas être vide."
    TOO_SHORT = "Le nom doit contenir au moins 2 caractères."
    TOO_LONG = "Le nom ne peut pas dépasser 100 caractères."
    INVALID_CHARS = "Le nom ne peut contenir que des lettres, espaces, tirets et apostrophes."


@dataclass(frozen=True)
class PersonName:
    """Représente un nom de personne validé."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError(NameValidationError.EMPTY_NAME.value)
        stripped = self.value.strip()
        # On remplace l'attribut value par la version strip dans un objet frozen
        object.__setattr__(self, 'value', stripped)

        if len(self.value) < 2:
            raise ValueError(NameValidationError.TOO_SHORT.value)
        if len(self.value) > 100:
            raise ValueError(NameValidationError.TOO_LONG.value)
        if not self._is_valid_characters(self.value):
            raise ValueError(NameValidationError.INVALID_CHARS.value)

    @staticmethod
    def _is_valid_characters(name: str) -> bool:
        # Lettres (y compris accentuées), espaces, tirets, apostrophes
        import re
        return bool(re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", name))

    def __str__(self) -> str:
        return self.value