"""
Entité domaine représentant une pièce détachée.
Contient son stock et son prix unitaire.
L'agence_id permet de lier la pièce à une agence pour le filtrage multi-agences.
"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional


@dataclass
class PieceDetachee:
    """
    Pièce détachée utilisée dans les interventions de maintenance.
    """
    reference: str          # obligatoire
    nom: str                # obligatoire
    prix_unitaire: Decimal  # obligatoire
    stock: int = 0          # optionnel
    agence_id: Optional[UUID] = None  # champ pour le multi-agences
    id: UUID = field(default_factory=uuid4)

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
        """
        Réduit le stock de la pièce.
        """
        if quantite > self.stock:
            raise ValueError("Stock insuffisant")
        self.stock -= quantite