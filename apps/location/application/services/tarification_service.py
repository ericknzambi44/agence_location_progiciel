from uuid import UUID
from decimal import Decimal
from datetime import date
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository
from location.domain.entities.regle_tarification import ReglesTarification


class TarificationService:
    def __init__(self, repo: RegleTarificationRepository):
        self.repo = repo

    def get_regles(self, agence_id: UUID) -> ReglesTarification:
        return self.repo.get(agence_id) or ReglesTarification(agence_id=agence_id, regles=[])

    def sauvegarder_regles(self, regles: ReglesTarification) -> None:
        self.repo.save(regles)

    def calculer_prix(self, agence_id: UUID, prix_base: Decimal, duree: int,
                      type_bien_id: UUID, date_debut: date) -> Decimal:
        regles = self.repo.get(agence_id)
        if regles is None:
            return prix_base
        return regles.calculer_prix(prix_base, duree, type_bien_id, date_debut)