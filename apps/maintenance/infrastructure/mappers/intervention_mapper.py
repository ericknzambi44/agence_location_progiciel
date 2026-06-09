from maintenance.domain.entities.intervention import Intervention, StatutIntervention
from maintenance.infrastructure.models import InterventionModel
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper

class InterventionMapper:
    @staticmethod
    def to_domain(model: InterventionModel) -> Intervention:
        technicien = TechnicienMapper.to_domain(model.technicien) if model.technicien else None
        return Intervention(
            id=model.id,
            bien_id=model.bien_id,
            technicien=technicien,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            statut=StatutIntervention(model.statut),
            cout_main_oeuvre=model.cout_main_oeuvre,
            cout_total=model.cout_total,
            pieces_utilisees=[],   # les pièces sont gérées séparément
        )

    @staticmethod
    def to_model(intervention: Intervention, include_id: bool = False) -> InterventionModel:
        model = InterventionModel(
            bien_id=intervention.bien_id,
            technicien_id=intervention.technicien.id if intervention.technicien else None,
            date_debut=intervention.date_debut,
            date_fin=intervention.date_fin,
            statut=intervention.statut.value,
            cout_main_oeuvre=intervention.cout_main_oeuvre,
            cout_total=intervention.cout_total
        )
        if include_id:
            model.id = intervention.id
        return model