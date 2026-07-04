"""
Use case pour lister les modules actifs.
Filtre par agence via l'agence_id passé en paramètre.
"""
from typing import List
from uuid import UUID
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.repositories.module_config_repository import ModuleConfigRepository


class ListerModulesActifsUseCase:
    """
    Use case pour récupérer la liste des modules actifs.
    """

    def __init__(self, repo: ModuleConfigRepository):
        self.repo = repo

    def execute(self, agence_id: UUID = None) -> List[ModuleConfig]:
        """
        Exécute le listing des modules actifs.

        Args:
            agence_id: UUID de l'agence (pour le filtrage).
                       Si None, retourne une liste vide (sauf superuser, géré dans le ViewSet).

        Returns:
            List[ModuleConfig]: Liste des configurations de modules actifs.
        """
        if agence_id is None:
            # Sécurité : on ne renvoie rien si agence_id non spécifié (sauf superuser)
            return []

        return self.repo.list_actifs(agence_id=agence_id)