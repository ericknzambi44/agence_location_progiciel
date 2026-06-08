from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from rh.domain.value_objects.note import Note
from typing import Optional

@dataclass
class Evaluation:
    id: UUID = field(default_factory=uuid4)
    employe_id: UUID
    date_evaluation: date
    note: Note
    commentaires: str = ""
    evaluateur_id: Optional[UUID] = None  # ID de l'employé qui évalue

    def __post_init__(self):
        if self.date_evaluation > date.today():
            raise ValueError("La date d'évaluation ne peut pas être dans le futur.")