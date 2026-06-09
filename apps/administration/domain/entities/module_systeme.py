from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List
from administration.domain.value_objects.code_module import CodeModule

@dataclass
class ModuleSysteme:
    id: UUID = field(default_factory=uuid4)
    code: CodeModule
    nom: str
    description: str = ""
    actif: bool = True
    dependances: List[CodeModule] = field(default_factory=list)  # codes des modules requis

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du module est obligatoire.")

    def activer(self):
        self.actif = True

    def desactiver(self):
        self.actif = False

    def a_dependance(self, code_module: CodeModule) -> bool:
        return any(d.value == code_module.value for d in self.dependances)