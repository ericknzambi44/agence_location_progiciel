"""
Use case : Retirer une pièce détachée d'une intervention.
Diminue la quantité de 1, ou supprime l'entrée si la quantité atteint 0.
Vérifie l'appartenance à l'agence.
"""
from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository


class RetirerPieceUseCase:
    def __init__(self, intervention_repo: InterventionRepository, piece_repo: PieceDetacheeRepository):
        self.intervention_repo = intervention_repo
        self.piece_repo = piece_repo

    def execute(self, intervention_id: UUID, piece_id: UUID, agence_id: UUID = None) -> None:
        """
        Retire une pièce d'une intervention.

        Args:
            intervention_id: UUID de l'intervention
            piece_id: UUID de la pièce à retirer
            agence_id: UUID de l'agence (pour vérification)

        Raises:
            ValueError: si l'intervention ou la pièce n'existent pas,
                        ou si elles n'appartiennent pas à l'agence.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour retirer une pièce.")

        # Récupérer l'intervention (avec vérification d'agence)
        intervention = self.intervention_repo.get(intervention_id, agence_id=agence_id)
        if not intervention:
            raise ValueError("Intervention introuvable ou non autorisée")

        # Récupérer la pièce (avec vérification d'agence)
        piece = self.piece_repo.get(piece_id, agence_id=agence_id)
        if not piece:
            raise ValueError("Pièce introuvable ou non autorisée")

        # Vérifier si la pièce est utilisée dans l'intervention
        for i, (p, q) in enumerate(intervention.pieces_utilisees):
            if p.id == piece.id:
                if q > 1:
                    intervention.pieces_utilisees[i] = (p, q - 1)
                else:
                    del intervention.pieces_utilisees[i]
                self.intervention_repo.update(intervention)
                return

        raise ValueError("Cette pièce n'est pas utilisée dans l'intervention")