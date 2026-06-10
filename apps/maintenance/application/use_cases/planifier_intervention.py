from datetime import datetime
from uuid import UUID
from maintenance.domain.entities.intervention import Intervention
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from stock.domain.repositories.bien_repository import BienRepository  # Pour vérifier état du bien

class PlanifierInterventionUseCase:
    def __init__(self, intervention_repo: InterventionRepository, technicien_repo: TechnicienRepository, bien_repo: BienRepository):
        self.intervention_repo = intervention_repo
        self.technicien_repo = technicien_repo
        self.bien_repo = bien_repo

    def execute(self, bien_id: UUID, technicien_id: UUID, date_debut: datetime, date_fin: datetime) -> Intervention:
        # Vérifier existence du bien et son état (doit être disponible ou en maintenance)
        bien = self.bien_repo.get(bien_id)
        if not bien:
            raise ValueError("Bien non trouvé")
        if bien.etat.value not in ['disponible', 'en_maintenance']:
            raise ValueError("Le bien n'est pas dans un état autorisant une intervention")

        technicien = self.technicien_repo.get(technicien_id)
        if not technicien:
            raise ValueError("Technicien non trouvé")

        # Vérifier chevauchement avec d'autres interventions
        interventions_existantes = self.intervention_repo.find_by_periode(date_debut, date_fin)
        intervention_temp = Intervention(bien_id=bien_id, technicien=technicien, date_debut=date_debut, date_fin=date_fin)
        for existing in interventions_existantes:
            if intervention_temp.est_en_conflit_avec(existing):
                raise ValueError("Conflit de planning : chevauchement avec une autre intervention")

        intervention = Intervention(
            bien_id=bien_id,
            technicien=technicien,
            date_debut=date_debut,
            date_fin=date_fin,
            statut='planifiee'
        )
        self.intervention_repo.add(intervention)
        return intervention