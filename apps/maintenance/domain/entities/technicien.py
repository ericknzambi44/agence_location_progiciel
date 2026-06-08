from dataclasses import dataclass
from uuid import UUID

from shared_kernel.domain.value_objects.email import Email
from shared_kernel.domain.value_objects.name import PersonName


@dataclass
class Technicien:
    id: UUID
    nom: PersonName
    email: Email
    specialite: str   # ex: "électricité", "plomberie", etc.
    cout_horaire: float   # en euros

    def __post_init__(self):
        if self.cout_horaire < 0:
            raise ValueError("Le coût horaire ne peut pas être négatif.")