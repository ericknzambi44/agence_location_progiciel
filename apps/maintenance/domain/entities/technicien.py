"""
Entité domaine représentant un technicien de maintenance.
Contient ses coordonnées et son coût horaire.
L'agence_id permet de lier le technicien à une agence pour le filtrage multi-agences.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4
from typing import Optional

from shared_kernel.domain.value_objects import Email, PersonName


@dataclass
class Technicien:
    """
    Technicien de maintenance.
    """
    nom: PersonName
    prenom: PersonName
    email: Email
    cout_horaire: Decimal
    agence_id: Optional[UUID] = None  # champ pour le multi-agences
    id: UUID = field(default_factory=uuid4)
    est_actif: bool = True

    def __post_init__(self):
        if self.cout_horaire < 0:
            raise ValueError("Le coût horaire ne peut pas être négatif")