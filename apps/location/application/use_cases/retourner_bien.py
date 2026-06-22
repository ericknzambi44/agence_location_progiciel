from uuid import UUID
from location.domain.repositories.contrat_repository import ContratRepository


class RetournerBienUseCase:
    def __init__(self, repo: ContratRepository):
        self.repo = repo

    def execute(self, contrat_id: UUID) -> None:
        contrat = self.repo.get(contrat_id)
        if not contrat:
            raise ValueError("Contrat introuvable.")
        if contrat.statut != "actif":
            raise ValueError("Seul un contrat actif peut être terminé.")
        contrat.terminer()
        self.repo.update(contrat)