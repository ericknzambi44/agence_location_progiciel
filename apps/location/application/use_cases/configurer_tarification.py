"""
Use case pour configurer les règles de tarification d'une agence.

Remplace l'ensemble des règles existantes par celles fournies.
L'agence_id est assigné directement sur l'agrégat avant la sauvegarde.
"""

from uuid import UUID

from location.domain.entities.regle_tarification import ReglesTarification
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository


class ConfigurerTarificationUseCase:
    """
    Use case pour enregistrer ou mettre à jour les règles de tarification.
    """

    def __init__(self, repo: RegleTarificationRepository):
        self.repo = repo

    def execute(self, agence_id: UUID, regles: ReglesTarification) -> None:
        """
        Exécute la configuration de la tarification.

        Args:
            agence_id (UUID): Identifiant de l'agence concernée.
            regles (ReglesTarification): Agrégat contenant les nouvelles règles.

        Raises:
            ValueError: si agence_id est None.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour configurer la tarification.")

        # L'agrégat doit être rattaché à l'agence
        regles.agence_id = agence_id

        # Persistance via le repository
        self.repo.save(regles)