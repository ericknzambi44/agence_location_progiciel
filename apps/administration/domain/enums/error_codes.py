from enum import Enum

class AgenceError(Enum):
    CODE_EXISTANT = "Ce code agence existe déjà."
    INTROUVABLE = "Agence non trouvée."
    NOM_REQUIS = "Le nom de l'agence est requis."

class ModuleError(Enum):
    CODE_EXISTANT = "Ce code module existe déjà."
    INTROUVABLE = "Module non trouvé."
    DEPENDANCE_MANQUANTE = "Impossible d'activer le module car une dépendance est inactive."
    MODULE_DEJA_ACTIF = "Le module est déjà actif."
    MODULE_DEJA_INACTIF = "Le module est déjà inactif."

class PermissionError(Enum):
    CODE_EXISTANT = "Cette permission existe déjà."
    INTROUVABLE = "Permission non trouvée."