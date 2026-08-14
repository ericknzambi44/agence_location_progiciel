"""
Use case pour terminer un contrat de location et marquer le bien comme retourné.

Vérifie que le contrat est actif, puis applique la logique métier de terminaison.
"""

from uuid import UUID

from location.domain.repositories.contrat_repository import ContratRepository


class RetournerBienUseCase:
    """
    Use case pour clôturer un contrat de location.
    """

    def __init__(self, repo: ContratRepository):
        self.repo = repo

    def execute(self, contrat_id: UUID) -> None:
        """
        Termine un contrat actif.

        Args:
            contrat_id (UUID): Identifiant du contrat.

        Raises:
            ValueError: si le contrat n'existe pas ou n'est pas actif.
        """
        contrat = self.repo.get(contrat_id)
        if not contrat:
            raise ValueError("Contrat introuvable.")

        if contrat.statut != "actif":
            raise ValueError("Seul un contrat actif peut être terminé.")

        # Logique métier de terminaison (définie dans l'entité Contrat)
        contrat.terminer()

        # Persistance de la modification
        self.repo.update(contrat)