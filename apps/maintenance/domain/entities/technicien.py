from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4
from shared_kernel.domain.value_objects import Email, PersonName

@dataclass
class Technicien:
    nom: PersonName
    prenom: PersonName
    email: Email
    cout_horaire: Decimal
    id: UUID = field(default_factory=uuid4)
    est_actif: bool = True

    def __post_init__(self):
        if self.cout_horaire < 0:
            raise ValueError("Le coût horaire ne peut pas être négatif")