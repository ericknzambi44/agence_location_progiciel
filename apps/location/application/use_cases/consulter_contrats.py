from typing import List
from location.domain.entities.contrat import Contrat
from location.domain.repositories.contrat_repository import ContratRepository


class ConsulterContratsUseCase:
    def __init__(self, repo: ContratRepository):
        self.repo = repo

    def execute(self) -> List[Contrat]:
        return self.repo.find_actifs()