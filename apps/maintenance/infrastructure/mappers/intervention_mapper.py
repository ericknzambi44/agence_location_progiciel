"""
Mapper entre l'entité domaine Intervention et le modèle ORM InterventionModel.
Assure la conversion dans les deux sens, incluant l'agence_id pour le multi-agences.
"""
from maintenance.domain.entities.intervention import Intervention
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import InterventionModel, InterventionPieceModel
from typing import List, Tuple


class InterventionMapper:
    """Conversion bidirectionnelle pour les interventions."""

    @staticmethod
    def to_domain(model: InterventionModel, technicien_repo, piece_repo) -> Intervention:
        """
        Construit une entité Intervention à partir du modèle Django.
        Inclut la récupération du technicien, des pièces et de l'agence_id.
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
            agence_id=model.agence_id  # <-- ajout de l'agence_id
        )
        intervention._cout_main_oeuvre = model.cout_main_oeuvre
        intervention._cout_total = model.cout_total
        return intervention

    @staticmethod
    def to_model(entity: Intervention) -> InterventionModel:
        """
        Construit un modèle Django à partir de l'entité Intervention.
        Inclut l'agence_id si présent.
        """
        kwargs = {
            'bien_id': entity.bien_id,
            'technicien_id': entity.technicien.id if entity.technicien else None,
            'date_debut': entity.date_debut,
            'date_fin': entity.date_fin,
            'statut': entity.statut,
            'cout_main_oeuvre': entity._cout_main_oeuvre,
            'cout_total': entity._cout_total,
            'agence_id': entity.agence_id  # <-- ajout
        }
        if entity.id is not None:
            kwargs['id'] = entity.id
        return InterventionModel(**kwargs)

    @staticmethod
    def save_pieces(model: InterventionModel, pieces: List[Tuple[PieceDetachee, int]]) -> None:
        """
        Sauvegarde les pièces associées à une intervention dans la table de liaison.
        """
        for piece, quantite in pieces:
            InterventionPieceModel.objects.create(
                intervention=model,
                piece_id=piece.id,
                quantite=quantite
            )