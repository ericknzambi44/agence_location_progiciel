from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional

@dataclass
class Categorie:
    id: UUID = field(default_factory=uuid4)
    nom: str
    description: Optional[str] = None
    parent: Optional['Categorie'] = None

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom de la catégorie est obligatoire.")
        self.nom = self.nom.strip()