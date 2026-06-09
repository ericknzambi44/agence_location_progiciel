from dataclasses import dataclass
from enum import Enum

class AdresseValidationError(Enum):
    RUE_VIDE = "La rue est obligatoire."
    VILLE_VIDE = "La ville est obligatoire."
    CODE_POSTAL_INVALIDE = "Le code postal doit comporter 5 chiffres."
    PAYS_VIDE = "Le pays est obligatoire."

@dataclass(frozen=True)
class Adresse:
    rue: str
    code_postal: str
    ville: str
    pays: str

    def __post_init__(self):
        if not self.rue or not self.rue.strip():
            raise ValueError(AdresseValidationError.RUE_VIDE.value)
        if not self.ville or not self.ville.strip():
            raise ValueError(AdresseValidationError.VILLE_VIDE.value)
        if not self.pays or not self.pays.strip():
            raise ValueError(AdresseValidationError.PAYS_VIDE.value)
        cp = self.code_postal.strip()
        import re
        if not re.match(r'^\d{5}$', cp):
            raise ValueError(AdresseValidationError.CODE_POSTAL_INVALIDE.value)