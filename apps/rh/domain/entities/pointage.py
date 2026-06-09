from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

class TypePointage:
    ENTRY = "ENTRY"
    EXIT = "EXIT"

@dataclass
class Pointage:
    employe_id: UUID
    type: str
    horodatage: datetime = field(default_factory=datetime.now)
    commentaire: str = ""
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.type not in (TypePointage.ENTRY, TypePointage.EXIT):
            raise ValueError("Type de pointage invalide")