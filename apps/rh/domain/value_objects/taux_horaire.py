from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class TauxHoraireValidationError(Enum):
    NEGATIF = "Le taux horaire ne peut pas être négatif."
    TROP_GRAND = "Le taux horaire dépasse 1000 €/h."

@dataclass(frozen=True)
class TauxHoraire:
    valeur: Decimal

    def __post_init__(self):
        if self.valeur < 0:
            raise ValueError(TauxHoraireValidationError.NEGATIF.value)
        if self.valeur > Decimal('1000'):
            raise ValueError(TauxHoraireValidationError.TROP_GRAND.value)