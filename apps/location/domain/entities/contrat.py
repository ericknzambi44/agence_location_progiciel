from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional
from location.domain.value_objects.montant import Montant


@dataclass
class Contrat:
    client_id: UUID
    bien_id: UUID
    date_debut: date
    date_fin: date
    montant_total: Montant
    statut: str = "actif"
    agence_id: Optional[UUID] = None 
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.date_debut >= self.date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")
        if self.statut not in ("actif", "termine", "annule"):
            raise ValueError("Statut invalide.")

    def annuler(self):
        self.statut = "annule"

    def terminer(self):
        self.statut = "termine"