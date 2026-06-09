from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Dict, Any
from administration.domain.value_objects.code_module import CodeModule

@dataclass
class ModuleConfig:
    code: CodeModule
    nom: str
    description: str = ""
    active: bool = True
    ordre_affichage: int = 0
    parametres: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du module est obligatoire.")
        self.nom = self.nom.strip()

    def activer(self):
        self.active = True

    def desactiver(self):
        self.active = False

    def definir_parametre(self, cle: str, valeur: Any):
        self.parametres[cle] = valeur

    def obtenir_parametre(self, cle: str, defaut: Any = None):
        return self.parametres.get(cle, defaut)