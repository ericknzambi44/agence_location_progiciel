"""
Use case : Ajouter une pièce détachée à une intervention.

Vérifie l'existence de l'intervention et de la pièce,
ainsi que leur appartenance à la même agence.
"""

from uuid import UUID

from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository


class AjouterPieceUseCase:
    """
    Use case pour ajouter une pièce à une intervention.
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
        quantite: int,
        agence_id: UUID = None
    ) -> None:
        """
        Exécute l'ajout d'une pièce à une intervention.

        Args:
            intervention_id (UUID): Identifiant de l'intervention.
            piece_id (UUID): Identifiant de la pièce à ajouter.
            quantite (int): Quantité positive.
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Raises:
            ValueError: si l'intervention ou la pièce n'existent pas,
                        si elles n'appartiennent pas à l'agence,
                        ou si l'opération est interdite.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour ajouter une pièce.")

        # Récupérer l'intervention (avec vérification d'agence)
        intervention = self.intervention_repo.get(intervention_id, agence_id=agence_id)
        if not intervention:
            raise ValueError("Intervention introuvable ou non autorisée pour votre agence.")

        # Récupérer la pièce (avec vérification d'agence)
        piece = self.piece_repo.get(piece_id, agence_id=agence_id)
        if not piece:
            raise ValueError("Pièce détachée introuvable ou non autorisée pour votre agence.")

        # Logique métier
        intervention.ajouter_piece(piece, quantite)

        # Persister
        self.intervention_repo.update(intervention)