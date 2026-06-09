from datetime import datetime
from uuid import UUID
from maintenance.domain.entities.intervention import Intervention, StatutIntervention
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from maintenance.domain.enums.error_codes import PlanificationError
from stock.infrastructure.models import BienModel  # ← contournement temporaire

class PlanifierInterventionUseCase:
    def __init__(self, intervention_repo: InterventionRepository,
                 technicien_repo: TechnicienRepository,
                 bien_repo=None):   # bien_repo non utilisé
        self.intervention_repo = intervention_repo
        self.technicien_repo = technicien_repo

    def execute(self, bien_id: UUID, technicien_id: UUID,
                date_debut: datetime, date_fin: datetime,
                description_panne: str = "") -> Intervention:
        # Récupérer le bien directement via le modèle (contournement)
        try:
            bien_model = BienModel.objects.get(id=bien_id)
        except BienModel.DoesNotExist:
            raise ValueError("Bien introuvable")
        
        # Vérifier l'état du bien
        if bien_model.etat not in ['disponible', 'endommage']:
            raise ValueError(PlanificationError.BIEN_INDISPONIBLE_POUR_MAINTENANCE.value)

        technicien = self.technicien_repo.get(technicien_id)
        if not technicien:
            raise ValueError("Technicien introuvable")

        conflits = self.intervention_repo.find_conflits(technicien_id, date_debut, date_fin)
        if conflits:
            raise ValueError(PlanificationError.CHEVAUCHEMENT_AVEC_AUTRE_INTERVENTION.value)

        intervention = Intervention(
            bien_id=bien_id,
            technicien=technicien,
            date_debut=date_debut,
            date_fin=date_fin,
            statut=StatutIntervention.PLANIFIEE
        )
        self.intervention_repo.add(intervention)
        return intervention