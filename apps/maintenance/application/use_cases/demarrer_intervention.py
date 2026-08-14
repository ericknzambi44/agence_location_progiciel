"""
Use case pour démarrer une intervention.
"""

from uuid import UUID

from maintenance.domain.repositories.intervention_repository import InterventionRepository


class DemarrerInterventionUseCase:
    """
    Use case pour démarrer une intervention planifiée.
    """

    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID, agence_id: UUID = None) -> None:
        """
        Démarre l'intervention.

        Args:
            intervention_id (UUID): Identifiant de l'intervention.
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Raises:
            ValueError: si l'intervention n'existe pas ou n'appartient pas à l'agence.
        """
        intervention = self.repo.get(intervention_id, agence_id=agence_id)
        if not intervention:
            raise ValueError("Intervention introuvable ou non autorisée.")

        intervention.demarrer()
        self.repo.update(intervention)