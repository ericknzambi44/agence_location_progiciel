"""
Entité représentant la configuration d'un module métier.
Contient son code, son nom, ses paramètres, et son état d'activation.
L'agence_id permet de lier la configuration à une agence pour le filtrage multi-agences.
"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Dict, Any, Optional
from administration.domain.value_objects.code_module import CodeModule


@dataclass
class ModuleConfig:
    """
    Configuration d'un module (ex: Stock, RH, Maintenance, etc.)
    """
    code: CodeModule
    nom: str
    description: str = ""
    active: bool = True
    ordre_affichage: int = 0
    parametres: Dict[str, Any] = field(default_factory=dict)
    agence_id: Optional[UUID] = None 
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom du module est obligatoire.")
        self.nom = self.nom.strip()

    def activer(self):
        """Active le module."""
        self.active = True

    def desactiver(self):
        """Désactive le module."""
        self.active = False

    def definir_parametre(self, cle: str, valeur: Any):
        """Définit un paramètre du module."""
        self.parametres[cle] = valeur

    def obtenir_parametre(self, cle: str, defaut: Any = None):
        """Récupère un paramètre du module."""
        return self.parametres.get(cle, defaut)