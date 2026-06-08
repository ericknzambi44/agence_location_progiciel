# extrait de intervention_mapper.py
from apps.maintenance.domain.entities.intervention import Intervention
from apps.maintenance.infrastructure.models import InterventionModel


@staticmethod
def to_domain(model: InterventionModel, technicien_repo, piece_repo) -> Intervention:
    technicien = technicien_repo.get(model.technicien_id) if model.technicien_id else None
    # Récupérer les pièces depuis la table de liaison
    pieces_models = model.interventionpiece_set.select_related('piece').all()
    pieces = []
    for ip in pieces_models:
        piece = piece_repo.get(ip.piece.id)  # ou directement mapper
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