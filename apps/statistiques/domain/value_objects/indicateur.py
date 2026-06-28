from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Indicateur:
    valeur: Decimal
    libelle: str
    unite: str  # €, %, nombre, heures, etc.