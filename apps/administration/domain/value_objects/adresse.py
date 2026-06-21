"""
Value Object représentant une adresse postale.
"""
from dataclasses import dataclass
from enum import Enum


class AdresseValidationError(Enum):
    LIGNE1_VIDE = "La ligne 1 de l'adresse est obligatoire."
    VILLE_VIDE = "La ville est obligatoire."
    CODE_POSTAL_INVALIDE = "Le code postal doit être alphanumérique et faire entre 3 et 10 caractères."


@dataclass(frozen=True)
class Adresse:
    ligne1: str           # <-- correspond à adresse_ligne1 dans le formulaire
    ligne2: str = ""      # <-- correspond à adresse_ligne2
    code_postal: str = ""
    ville: str = ""
    pays: str = "France"

    def __post_init__(self):
        if not self.ligne1 or not self.ligne1.strip():
            raise ValueError(AdresseValidationError.LIGNE1_VIDE.value)
        if not self.ville or not self.ville.strip():
            raise ValueError(AdresseValidationError.VILLE_VIDE.value)
        if self.code_postal and not self._code_postal_valide(self.code_postal):
            raise ValueError(AdresseValidationError.CODE_POSTAL_INVALIDE.value)

    @staticmethod
    def _code_postal_valide(cp: str) -> bool:
        import re
        return bool(re.match(r'^[A-Z0-9]{3,10}$', cp, re.IGNORECASE))