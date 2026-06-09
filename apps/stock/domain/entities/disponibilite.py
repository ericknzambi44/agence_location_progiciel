from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from stock.domain.entities.bien import Bien

@dataclass
class DisponibilitePeriode:
    bien: Bien
    date_debut: date
    date_fin: date
    est_reserve: bool = False
    reservation_id: UUID = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.date_debut > self.date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")