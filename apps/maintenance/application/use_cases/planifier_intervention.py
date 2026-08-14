"""
Use case pour planifier une nouvelle intervention.

Vérifie la disponibilité du bien et du technicien,
et assigne l'agence_id à l'intervention créée.
"""

from datetime import datetime
from uuid import UUID

from maintenance.domain.entities.intervention import Intervention
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from stock.domain.repositories.bien_repository import BienRepository


class PlanifierInterventionUseCase:
    """
    Use case pour planifier une intervention de maintenance.
    """

    def __init__(
        self,
        intervention_repo: InterventionRepository,
        technicien_repo: TechnicienRepository,
        bien_repo: BienRepository
    ):
        self.intervention_repo = intervention_repo
        self.technicien_repo = technicien_repo
        self.bien_repo = bien_repo

    def execute(
        self,
        bien_id: UUID,
        technicien_id: UUID,
        date_debut: datetime,
        date_fin: datetime,
        agence_id: UUID = None
    ) -> Intervention:
        """
        Planifie une intervention.

        Args:
            bien_id (UUID): Identifiant du bien.
            technicien_id (UUID): Identifiant du technicien.
            date_debut (datetime): Début de l'intervention.
            date_fin (datetime): Fin de l'intervention.
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Returns:
            Intervention: L'intervention créée.

        Raises:
            ValueError: Si données invalides, conflit, ou agence_id manquant.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour planifier une intervention.")

        # Vérifier le bien
        bien = self.bien_repo.get(bien_id, agence_id=agence_id)
        if not bien:
            raise ValueError("Bien non trouvé ou non autorisé pour votre agence.")
        if bien.etat.value not in ['disponible', 'en_maintenance']:
            raise ValueError("Le bien n'est pas dans un état autorisant une intervention.")

        # Vérifier le technicien
        technicien = self.technicien_repo.get(technicien_id, agence_id=agence_id)
        if not technicien:
            raise ValueError("Technicien non trouvé ou non autorisé pour votre agence.")

        # Vérifier les conflits de planning
        interventions_existantes = self.intervention_repo.find_by_periode(
            date_debut, date_fin, agence_id=agence_id
        )
        intervention_temp = Intervention(
            bien_id=bien_id,
            technicien=technicien,
            date_debut=date_debut,
            date_fin=date_fin
        )
        for existing in interventions_existantes:
            if intervention_temp.est_en_conflit_avec(existing):
                raise ValueError("Conflit de planning : chevauchement avec une autre intervention.")

        # Créer l'intervention
        intervention = Intervention(
            bien_id=bien_id,
            technicien=technicien,
            date_debut=date_debut,
            date_fin=date_fin,
            statut='planifiee',
            agence_id=agence_id
        )
        self.intervention_repo.add(intervention)
        return intervention