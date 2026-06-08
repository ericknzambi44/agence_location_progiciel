from datetime import datetime
from uuid import UUID
from maintenance.domain.entities.intervention import Intervention, StatutIntervention
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from stock.domain.repositories.bien_repository import BienRepository
from maintenance.domain.enums.error_codes import PlanificationError

class PlanifierInterventionUseCase:
    def __init__(self, intervention_repo: InterventionRepository, technicien_repo: TechnicienRepository, bien_repo: BienRepository):
        self.intervention_repo = intervention_repo
        self.technicien_repo = technicien_repo
        self.bien_repo = bien_repo

    def execute(self, bien_id: UUID, technicien_id: UUID, debut: datetime, fin: datetime, description_panne: str) -> Intervention:
        # Récupérer le bien
        bien = self.bien_repo.get(bien_id)
        if not bien:
            raise ValueError("Bien introuvable")
        # Vérifier disponibilité du bien (état et non déjà en intervention)
        if bien.etat.value not in ['disponible', 'endommage']:  # on peut intervenir sur un bien endommagé
            raise ValueError(PlanificationError.BIEN_INDISPONIBLE_POUR_MAINTENANCE.value)
        # Vérifier disponibilité technicien
        technicien = self.technicien_repo.get(technicien_id)
        if not technicien:
            raise ValueError("Technicien introuvable")
        conflits = self.intervention_repo.find_conflits(technicien_id, debut, fin)
        if conflits:
            raise ValueError(PlanificationError.CHEVAUCHEMENT_AVEC_AUTRE_INTERVENTION.value)
        # Créer intervention
        intervention = Intervention(
            bien=bien,
            description_panne=description_panne,
            statut=StatutIntervention.PLANIFIEE
        )
        intervention.planifier(debut, fin, technicien)
        self.intervention_repo.add(intervention)
        return intervention