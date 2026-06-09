from maintenance.domain.entities.intervention import Intervention, StatutIntervention
from maintenance.infrastructure.models import InterventionModel, InterventionPieceModel
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper
from maintenance.infrastructure.mappers.piece_mapper import PieceDetacheeMapper
from stock.infrastructure.repositories.django_bien_repository import DjangoBienRepository  # si nécessaire
from uuid import UUID

class InterventionMapper:
    @staticmethod
    def to_domain(model: InterventionModel, technicien_repo=None, piece_repo=None):
        from maintenance.domain.entities.intervention import Intervention
        from maintenance.domain.entities.technicien import Technicien
        from maintenance.domain.entities.piece_detachee import PieceDetachee
        
        technicien = None
        if technicien_repo and model.technicien_id:
            technicien = technicien_repo.get(model.technicien_id)
        pieces = []
        if piece_repo:
            for ip in model.interventionpiece_set.all():
                piece = piece_repo.get(ip.piece_id)
                pieces.append((piece, ip.quantite))
        
        return Intervention(
            bien_id=model.bien_id,
            technicien=technicien,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            statut=StatutIntervention(model.statut),
            pieces_utilisees=pieces,
            cout_main_oeuvre=model.cout_main_oeuvre,
            cout_total=model.cout_total,
            id=model.id
        )

    @staticmethod
    def to_model(intervention: Intervention):
        model = InterventionModel(
            id=intervention.id,
            bien_id=intervention.bien_id,
            technicien_id=intervention.technicien.id if intervention.technicien else None,
            date_debut=intervention.date_debut,
            date_fin=intervention.date_fin,
            statut=intervention.statut.value,
            cout_main_oeuvre=intervention.cout_main_oeuvre,
            cout_total=intervention.cout_total
        )
        return model