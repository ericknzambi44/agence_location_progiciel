"""
Mapper entre l'entité domaine Intervention et le modèle ORM Intervention.

Assure la conversion bidirectionnelle, incluant l'agence_id pour le multi-agences.
"""

from typing import List, Tuple

from maintenance.domain.entities.intervention import Intervention  # Entité domaine
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import Intervention as InterventionModel  # Modèle Django
from maintenance.infrastructure.models import InterventionPiece


class InterventionMapper:
    """Conversion bidirectionnelle pour les interventions."""

    @staticmethod
    def to_domain(model: InterventionModel, technicien_repo, piece_repo) -> Intervention:
        """
        Construit une entité Intervention à partir du modèle Django.

        Args:
            model (InterventionModel): Instance du modèle ORM.
            technicien_repo : Repository pour récupérer le technicien.
            piece_repo : Repository pour récupérer les pièces.

        Returns:
            Intervention: Entité domaine.
        """
        technicien = technicien_repo.get(model.technicien_id) if model.technicien_id else None

        pieces_models = model.pieces.select_related('piece').all()
        pieces = []
        for ip in pieces_models:
            piece = piece_repo.get(ip.piece.id)
            if piece:
                pieces.append((piece, ip.quantite))

        intervention = Intervention(
            id=model.id,
            bien_id=model.bien_id,
            technicien=technicien,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            statut=model.statut,
            pieces_utilisees=pieces,
            agence_id=model.agence_id
        )
        intervention._cout_main_oeuvre = model.cout_main_oeuvre
        intervention._cout_total = model.cout_total
        return intervention

    @staticmethod
    def to_model(entity: Intervention) -> InterventionModel:
        """
        Construit un modèle Django à partir de l'entité Intervention.

        Important :
            - Utilise `technicien_id` (identifiant) et non `technicien` (objet).
            - L'objet `Technicien` du domaine n'est pas une instance du modèle Django.

        Args:
            entity (Intervention): Entité domaine.

        Returns:
            InterventionModel: Instance du modèle ORM (non persistée).
        """
        kwargs = {
            'bien_id': entity.bien_id,
            'technicien_id': entity.technicien.id if entity.technicien else None,
            'date_debut': entity.date_debut,
            'date_fin': entity.date_fin,
            'statut': entity.statut,
            'cout_main_oeuvre': getattr(entity, '_cout_main_oeuvre', 0),
            'cout_total': getattr(entity, '_cout_total', 0),
            'agence_id': entity.agence_id
        }
        if entity.id is not None:
            kwargs['id'] = entity.id
        return InterventionModel(**kwargs)

    @staticmethod
    def save_pieces(model: InterventionModel, pieces: List[Tuple[PieceDetachee, int]]) -> None:
        """
        Sauvegarde les pièces associées à une intervention dans la table de liaison.

        Args:
            model (InterventionModel): Instance du modèle ORM déjà sauvegardée.
            pieces (List[Tuple[PieceDetachee, int]]): Liste des pièces et quantités.
        """
        for piece, quantite in pieces:
            InterventionPiece.objects.create(
                intervention=model,
                piece_id=piece.id,
                quantite=quantite
            )