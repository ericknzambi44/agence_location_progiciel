"""
Use case : Retirer une pièce détachée d'une intervention.

Diminue la quantité de 1, ou supprime l'entrée si la quantité atteint 0.
Vérifie l'appartenance à l'agence.
"""

from uuid import UUID

from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository


class RetirerPieceUseCase:
    """
    Use case pour retirer une pièce d'une intervention.
    """

    def __init__(
        self,
        intervention_repo: InterventionRepository,
        piece_repo: PieceDetacheeRepository
    ):
        self.intervention_repo = intervention_repo
        self.piece_repo = piece_repo

    def execute(
        self,
        intervention_id: UUID,
        piece_id: UUID,
        agence_id: UUID = None
    ) -> None:
        """
        Retire une pièce d'une intervention.

        Args:
            intervention_id (UUID): Identifiant de l'intervention.
            piece_id (UUID): Identifiant de la pièce à retirer.
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Raises:
            ValueError: si l'intervention ou la pièce n'existent pas,
                        ou si elles n'appartiennent pas à l'agence.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour retirer une pièce.")

        intervention = self.intervention_repo.get(intervention_id, agence_id=agence_id)
        if not intervention:
            raise ValueError("Intervention introuvable ou non autorisée.")

        piece = self.piece_repo.get(piece_id, agence_id=agence_id)
        if not piece:
            raise ValueError("Pièce introuvable ou non autorisée.")

        # Chercher la pièce dans les pièces utilisées
        for i, (p, q) in enumerate(intervention.pieces_utilisees):
            if p.id == piece.id:
                if q > 1:
                    intervention.pieces_utilisees[i] = (p, q - 1)
                else:
                    del intervention.pieces_utilisees[i]
                self.intervention_repo.update(intervention)
                return

        raise ValueError("Cette pièce n'est pas utilisée dans l'intervention.")