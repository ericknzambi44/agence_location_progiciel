from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from pyparsing import Optional
from stock.domain.entities.bien import Bien
from stock.domain.value_objects.quantite import Quantite

class TypeMouvement(Enum):
    ENTREE = "entree"
    SORTIE = "sortie"
    RESERVATION = "reservation"
    ANNULATION_RESERVATION = "annulation_reservation"
    RETOUR = "retour"

@dataclass
class MouvementStock:
    id: UUID = field(default_factory=uuid4)
    bien: Bien
    quantite: Quantite
    type_mouvement: TypeMouvement
    date_heure: datetime = field(default_factory=datetime.now)
    reference_document: Optional[str] = None  # numéro de location, facture, etc.
    commentaire: Optional[str] = None

    def __post_init__(self):
        if self.quantite.value <= 0:
            raise ValueError("La quantité d'un mouvement doit être > 0")
        # La validation de cohérence (ex: stock suffisant) relève du use case