"""
Value Object : Matricule.

Représente le matricule unique d'un employé.

Règles :
    - Ne peut pas être vide.
    - Longueur comprise entre 2 et 20 caractères après normalisation.
    - Caractères autorisés : lettres (A-Z, a-z), chiffres (0-9), tiret (-), underscore (_).
    - La valeur est automatiquement mise en majuscules.
"""

from dataclasses import dataclass
from enum import Enum
import re


class MatriculeValidationError(Enum):
    VIDE = "Le matricule ne peut pas être vide."
    FORMAT_INVALIDE = (
        "Le matricule doit contenir entre 2 et 20 caractères, composés de lettres, "
        "chiffres, tirets ou underscores."
    )


@dataclass(frozen=True)
class Matricule:
    value: str

    def __post_init__(self):
        """
        Valide et normalise le matricule.
        """
        if not self.value or not self.value.strip():
            raise ValueError(MatriculeValidationError.VIDE.value)

        # Normalisation : suppression des espaces superflus et mise en majuscules
        val = self.value.strip().upper()
        object.__setattr__(self, 'value', val)

        if len(val) < 2 or len(val) > 20:
            raise ValueError(MatriculeValidationError.FORMAT_INVALIDE.value)

        if not re.match(r'^[A-Z0-9_-]+$', val):
            raise ValueError(MatriculeValidationError.FORMAT_INVALIDE.value)