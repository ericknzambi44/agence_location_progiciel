from typing import List
from uuid import UUID
from location.domain.entities.contrat import Contrat
from location.domain.repositories.contrat_repository import ContratRepository


class ConsulterContratsUseCase:
    def __init__(self, repo: ContratRepository):
        self.repo = repo

    def execute(self, agence_id: UUID = None) -> List[Contrat]:
        return self.repo.find_actifs(agence_id=agence_id)