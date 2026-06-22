from uuid import UUID
from location.domain.entities.regle_tarification import ReglesTarification
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository


class ConfigurerTarificationUseCase:
    def __init__(self, repo: RegleTarificationRepository):
        self.repo = repo

    def execute(self, agence_id: UUID, regles: ReglesTarification) -> None:
       
        regles.agence_id = agence_id
        self.repo.save(regles)