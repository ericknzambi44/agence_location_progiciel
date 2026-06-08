from dataclasses import dataclass, field
from uuid import UUID, uuid4
from maintenance.domain.value_objects.cout import Cout

@dataclass
class PieceDetachee:
    id: UUID = field(default_factory=uuid4)
    reference: str
    nom: str
    prix_unitaire: Cout
    quantite_utilisee: int = 1

    def __post_init__(self):
        if not self.reference.strip():
            raise ValueError("La référence de la pièce est obligatoire.")
        if self.quantite_utilisee <= 0:
            raise ValueError("La quantité doit être positive.")