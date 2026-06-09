from dataclasses import dataclass, field
from uuid import UUID, uuid4
from shared_kernel.domain.value_objects import Email, PersonName
from decimal import Decimal

@dataclass
class Technicien:
    nom: PersonName
    prenom: PersonName
    email: Email
    cout_horaire: Decimal
    actif: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.cout_horaire < 0:
            raise ValueError("Le coût horaire ne peut pas être négatif.")