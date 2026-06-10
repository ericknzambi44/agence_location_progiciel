from maintenance.domain.entities.intervention import Intervention
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import InterventionModel, InterventionPieceModel
from typing import List, Tuple

class InterventionMapper:
    @staticmethod
    def to_domain(model: InterventionModel, technicien_repo, piece_repo) -> Intervention:
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
            pieces_utilisees=pieces
        )
        intervention._cout_main_oeuvre = model.cout_main_oeuvre
        intervention._cout_total = model.cout_total
        return intervention

    @staticmethod
    def to_model(entity: Intervention) -> InterventionModel:
        kwargs = {
            'bien_id': entity.bien_id,
            'technicien_id': entity.technicien.id if entity.technicien else None,
            'date_debut': entity.date_debut,
            'date_fin': entity.date_fin,
            'statut': entity.statut,
            'cout_main_oeuvre': entity._cout_main_oeuvre,
            'cout_total': entity._cout_total,
        }
        if entity.id is not None:
            kwargs['id'] = entity.id
        return InterventionModel(**kwargs)

    @staticmethod
    def save_pieces(model: InterventionModel, pieces: List[Tuple[PieceDetachee, int]]) -> None:
        for piece, quantite in pieces:
            InterventionPieceModel.objects.create(
                intervention=model,
                piece_id=piece.id,
                quantite=quantite
            )