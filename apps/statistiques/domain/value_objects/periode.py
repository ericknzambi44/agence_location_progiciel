"""
Value Object représentant une période (jour, mois, année).
"""
from dataclasses import dataclass
from datetime import date
from enum import Enum

class UnitePeriode(Enum):
    JOUR = "jour"
    MOIS = "mois"
    ANNEE = "annee"

@dataclass(frozen=True)
class Periode:
    debut: date
    fin: date
    unite: UnitePeriode

    def __post_init__(self):
        if self.debut > self.fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")