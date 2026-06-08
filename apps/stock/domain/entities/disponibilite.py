from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from stock.domain.entities.bien import Bien

@dataclass
class DisponibilitePeriode:
    id: UUID = field(default_factory=uuid4)
    bien: Bien
    date_debut: date
    date_fin: date
    est_reserve: bool = False
    reservation_id: Optional[UUID] = None  # lien vers un contrat de location

    def __post_init__(self):
        if self.date_debut > self.date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")
        if self.date_debut < date.today():
            # On pourrait autoriser une planification rétroactive selon besoin métier
            pass