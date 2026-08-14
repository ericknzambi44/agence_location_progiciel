"""
Use case pour vérifier la disponibilité des biens sur une période.
"""

from datetime import date
from typing import List
from uuid import UUID

from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien


class VerifierDisponibiliteUseCase:
    """
    Use case de vérification de disponibilité.
    """

    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, debut: date, fin: date, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne les biens disponibles sur la période, filtrés par agence.

        Args:
            debut (date): Date de début.
            fin (date): Date de fin.
            agence_id (UUID, optionnel): Agence pour l'isolation.

        Returns:
            List[Bien]: Biens disponibles.
        """
        return self.repo.find_disponibles_periode(debut, fin, agence_id=agence_id)