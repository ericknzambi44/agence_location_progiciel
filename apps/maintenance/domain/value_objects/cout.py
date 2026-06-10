from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Cout:
    valeur: Decimal   

    def __post_init__(self):
        if self.valeur < 0:
            raise ValueError("Le coût ne peut pas être négatif")