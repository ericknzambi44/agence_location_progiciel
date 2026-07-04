from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional
from administration.domain.value_objects.telephone import Telephone
from shared_kernel.domain.value_objects import Email, PersonName



@dataclass
class Client:
    nom: PersonName
    prenom: PersonName
    email: Email
    telephone: Telephone
    adresse: str
    agence_id: Optional[UUID] = None
    id: UUID = field(default_factory=uuid4)
    est_actif: bool = True

    def __post_init__(self):
        if not self.adresse or not self.adresse.strip():
            raise ValueError("L'adresse du client est obligatoire.")