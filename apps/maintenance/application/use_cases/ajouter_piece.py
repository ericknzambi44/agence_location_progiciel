from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository

class AjouterPieceUseCase:
    def __init__(self, intervention_repo: InterventionRepository, piece_repo: PieceDetacheeRepository):
        self.intervention_repo = intervention_repo
        self.piece_repo = piece_repo

    def execute(self, intervention_id: UUID, piece_id: UUID, quantite: int) -> None:
        intervention = self.intervention_repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")
        piece = self.piece_repo.get(piece_id)
        if not piece:
            raise ValueError("Pièce détachée introuvable")
        intervention.ajouter_piece(piece, quantite)
        self.intervention_repo.update(intervention)