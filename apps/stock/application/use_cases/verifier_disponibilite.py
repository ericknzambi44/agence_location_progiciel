from datetime import date
from typing import List
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien

class VerifierDisponibiliteUseCase:
    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, debut: date, fin: date) -> List[Bien]:
        return self.repo.find_disponibles_periode(debut, fin)