"""
Use case : Ajouter une pièce détachée à une intervention.
Vérifie l'existence de l'intervention et de la pièce,
puis appelle la méthode métier de l'entité Intervention.
"""
from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository


class AjouterPieceUseCase:
    def __init__(
        self,
        intervention_repo: InterventionRepository,
        piece_repo: PieceDetacheeRepository
    ):
        self.intervention_repo = intervention_repo
        self.piece_repo = piece_repo

    def execute(self, intervention_id: UUID, piece_id: UUID, quantite: int) -> None:
        """
        Exécute l'ajout d'une pièce à une intervention.

        Args:
            intervention_id: UUID de l'intervention cible
            piece_id: UUID de la pièce à ajouter
            quantite: quantité (positive)

        Raises:
            ValueError: si l'intervention ou la pièce n'existent pas,
                        ou si l'opération est interdite (métier).
        """
        # Récupérer l'intervention
        intervention = self.intervention_repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")

        # Récupérer la pièce
        piece = self.piece_repo.get(piece_id)
        if not piece:
            raise ValueError("Pièce détachée introuvable")

        # Délégation à la logique métier de l'entité
        intervention.ajouter_piece(piece, quantite)

        # Persister les modifications
        self.intervention_repo.update(intervention)