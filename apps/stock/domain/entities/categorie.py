from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional

@dataclass
class Categorie:
    # Champs obligatoires (sans valeur par défaut)
    nom: str
    # Champs optionnels (avec valeur par défaut)
    description: Optional[str] = None
    parent: Optional['Categorie'] = None
    # id en dernier avec default_factory
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom de la catégorie est obligatoire.")
        self.nom = self.nom.strip()