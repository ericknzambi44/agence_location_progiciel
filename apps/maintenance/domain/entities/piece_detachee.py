from dataclasses import dataclass, field
from uuid import UUID, uuid4
from decimal import Decimal

@dataclass
class PieceDetachee:
    reference: str          # obligatoire
    nom: str                # obligatoire
    prix_unitaire: Decimal  # obligatoire
    stock: int = 0          # optionnel
    id: UUID = field(default_factory=uuid4)  # dernier

    def __post_init__(self):
        if not self.reference or not self.reference.strip():
            raise ValueError("La référence est obligatoire")
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom est obligatoire")
        if self.prix_unitaire < 0:
            raise ValueError("Le prix unitaire ne peut pas être négatif")
        if self.stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")

    def reduire_stock(self, quantite: int):
        if quantite > self.stock:
            raise ValueError("Stock insuffisant")
        self.stock -= quantite