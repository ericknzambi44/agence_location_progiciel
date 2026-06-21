from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email


@dataclass
class Agence:
    code: CodeAgence
    nom: str
    adresse: Adresse
    telephone: Telephone
    email: Email
    actif: bool = True
    date_creation: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom de l'agence est obligatoire.")