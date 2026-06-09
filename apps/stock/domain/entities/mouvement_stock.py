from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from stock.domain.entities.bien import Bien
from stock.domain.value_objects.quantite import Quantite
from enum import Enum

class TypeMouvement(Enum):
    ENTREE = "entree"
    SORTIE = "sortie"
    RESERVATION = "reservation"
    ANNULATION_RESERVATION = "annulation_reservation"
    RETOUR = "retour"

@dataclass
class MouvementStock:
    bien: Bien
    quantite: Quantite
    type_mouvement: TypeMouvement
    reference_document: str = None
    commentaire: str = None
    date_heure: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.quantite.value <= 0:
            raise ValueError("La quantité d'un mouvement doit être > 0")