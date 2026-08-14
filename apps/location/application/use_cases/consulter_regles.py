"""
Use case pour consulter les règles de tarification d'une agence.

Retourne l'agrégat ReglesTarification (vide si aucune règle n'est définie).
"""

from uuid import UUID

from location.domain.entities.regle_tarification import ReglesTarification
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository


class ConsulterReglesUseCase:
    """
    Use case de lecture des règles de tarification.
    """

    def __init__(self, repo: RegleTarificationRepository):
        self.repo = repo

    def execute(self, agence_id: UUID) -> ReglesTarification:
        """
        Récupère les règles de tarification pour une agence donnée.

        Args:
            agence_id (UUID): Identifiant de l'agence.

        Returns:
            ReglesTarification: Agrégat contenant la liste des règles (vide si aucune).

        Raises:
            ValueError: si agence_id est None.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour consulter les règles.")

        regles = self.repo.get(agence_id)
        if regles is None:
            regles = ReglesTarification(agence_id=agence_id, regles=[])
        return regles