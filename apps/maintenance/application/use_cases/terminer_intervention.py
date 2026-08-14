"""
Use case pour terminer une intervention.

Calcule le coût de base, puis applique les règles de tarification configurées.
"""

from decimal import Decimal
from uuid import UUID
from datetime import date

from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.application.services.tarification_maintenance_service import TarificationMaintenanceService
from maintenance.domain.value_objects.duree import Duree
from maintenance.domain.value_objects.cout import Cout


class TerminerInterventionUseCase:
    """
    Use case pour terminer une intervention et calculer le coût final.
    """

    def __init__(
        self,
        repo: InterventionRepository,
        tarif_service: TarificationMaintenanceService
    ):
        self.repo = repo
        self.tarif_service = tarif_service

    def execute(
        self,
        intervention_id: UUID,
        agence_id: UUID,
        date_intervention: date
    ) -> float:
        """
        Termine l'intervention et applique les règles de tarification.

        Args:
            intervention_id (UUID): Identifiant de l'intervention.
            agence_id (UUID): Identifiant de l'agence (pour les règles).
            date_intervention (date): Date de l'intervention.

        Returns:
            float: Coût total final.

        Raises:
            ValueError: si l'intervention n'existe pas ou n'appartient pas à l'agence.
        """
        intervention = self.repo.get(intervention_id, agence_id=agence_id)
        if not intervention:
            raise ValueError("Intervention introuvable ou non autorisée.")

        # Calculer le coût de base (main-d'œuvre + pièces)
        cout_base_float = intervention.calculer_cout()
        cout_base = Cout(Decimal(str(cout_base_float)))

        # Durée
        if not intervention.date_debut or not intervention.date_fin:
            raise ValueError("Les dates de l'intervention ne sont pas définies.")
        duree_heures = (intervention.date_fin - intervention.date_debut).total_seconds() / 3600
        duree = Duree(duree_heures)

        # Application des règles de tarification
        cout_final = self.tarif_service.appliquer_regles(
            agence_id=agence_id,
            cout_base=cout_base,
            duree=duree,
            date_intervention=date_intervention
        )

        # Mise à jour de l'entité
        intervention._cout_total = cout_final.valeur
        intervention.statut = "terminee"

        # Persistance
        self.repo.update(intervention)

        return float(cout_final.valeur)