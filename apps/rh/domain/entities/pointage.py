from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from rh.domain.entities.employe import Employe

class TypePointage:
    ENTRY = "ENTRY"
    EXIT = "EXIT"

@dataclass
class Pointage:
    id: UUID = field(default_factory=uuid4)
    employe_id: UUID
    horodatage: datetime = field(default_factory=datetime.now)
    type: str  # ENTRY ou EXIT
    commentaire: str = ""

    def __post_init__(self):
        if self.type not in (TypePointage.ENTRY, TypePointage.EXIT):
            raise ValueError("Type de pointage invalide")
        # On pourrait vérifier qu'un ENTRY n'est pas suivi d'un autre ENTRY (logique métier plus complexe à mettre dans use case)