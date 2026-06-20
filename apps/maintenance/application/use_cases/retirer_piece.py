from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository

class RetirerPieceUseCase:
    def __init__(self, intervention_repo: InterventionRepository, piece_repo: PieceDetacheeRepository):
        self.intervention_repo = intervention_repo
        self.piece_repo = piece_repo

    def execute(self, intervention_id: UUID, piece_id: UUID) -> None:
        intervention = self.intervention_repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")

        piece = self.piece_repo.get(piece_id)
        if not piece:
            raise ValueError("Pièce introuvable")

        # Vérifier si la pièce est utilisée
        for i, (p, q) in enumerate(intervention.pieces_utilisees):
            if p.id == piece.id:
                if q > 1:
                    intervention.pieces_utilisees[i] = (p, q - 1)
                else:
                    del intervention.pieces_utilisees[i]
                self.intervention_repo.update(intervention)
                return

        raise ValueError("Cette pièce n'est pas utilisée dans l'intervention")