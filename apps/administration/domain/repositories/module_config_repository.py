"""
Repository abstrait pour la configuration des modules.
Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule


class ModuleConfigRepository(ABC):
    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[ModuleConfig]:
        """
        Récupère une configuration de module par son ID.
        Si agence_id est fourni, filtre par agence.
        """
        pass

    @abstractmethod
    def get_by_code(self, code: CodeModule, agence_id: UUID = None) -> Optional[ModuleConfig]:
        """
        Récupère une configuration par son code.
        Si agence_id est fourni, filtre par agence.
        """
        pass

    @abstractmethod
    def add(self, config: ModuleConfig) -> None:
        """
        Ajoute une nouvelle configuration (l'agence_id doit être défini dans l'entité).
        """
        pass

    @abstractmethod
    def update(self, config: ModuleConfig) -> None:
        """
        Met à jour une configuration existante.
        """
        pass

    @abstractmethod
    def list_all(self, agence_id: UUID = None) -> List[ModuleConfig]:
        """
        Liste toutes les configurations.
        Si agence_id est fourni, filtre par agence.
        Si agence_id est None, retourne une liste vide (sauf pour superuser).
        """
        pass

    @abstractmethod
    def list_actifs(self, agence_id: UUID = None) -> List[ModuleConfig]:
        """
        Liste les configurations actives.
        Si agence_id est fourni, filtre par agence.
        Si agence_id est None, retourne une liste vide (sauf pour superuser).
        """
        pass