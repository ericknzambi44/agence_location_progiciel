"""
Use case pour consulter la liste des contrats d'une agence.

Retourne uniquement les contrats actifs de l'agence, via le repository.
"""

from typing import List
from uuid import UUID

from location.domain.entities.contrat import Contrat
from location.domain.repositories.contrat_repository import ContratRepository


class ConsulterContratsUseCase:
    """
    Use case de lecture des contrats actifs d'une agence.
    """

    def __init__(self, repo: ContratRepository):
        self.repo = repo

    def execute(self, agence_id: UUID = None) -> List[Contrat]:
        """
        Retourne les contrats actifs pour une agence donnée.

        Args:
            agence_id (UUID, optionnel): Identifiant de l'agence.
                Si None, le repository doit retourner une liste vide (sécurité).

        Returns:
            List[Contrat]: Liste des contrats actifs.
        """
        return self.repo.find_actifs(agence_id=agence_id)