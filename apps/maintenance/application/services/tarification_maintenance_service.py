"""
Service de tarification pour la maintenance.
Applique les règles de tarification (remises, majorations, forfaits) sur le coût d'une intervention.
"""
from uuid import UUID
from decimal import Decimal
from datetime import date
from maintenance.domain.repositories.regle_maintenance_repository import RegleMaintenanceRepository
from maintenance.domain.entities.regle_maintenance import ReglesMaintenance
from maintenance.domain.value_objects.duree import Duree
from maintenance.domain.value_objects.cout import Cout


class TarificationMaintenanceService:
    """
    Service métier pour la gestion et l'application des règles de tarification de maintenance.
    """

    def __init__(self, repo: RegleMaintenanceRepository):
        self.repo = repo

    def get_regles(self, agence_id: UUID = None) -> ReglesMaintenance:
        """
        Récupère les règles de tarification pour une agence donnée.
        Retourne un agrégat vide si aucune règle n'est définie.
        """
        if agence_id is None:
            return ReglesMaintenance(agence_id=None, regles=[])  # ou lever une erreur
        regles = self.repo.get(agence_id)
        if regles is None:
            regles = ReglesMaintenance(agence_id=agence_id, regles=[])
        return regles

    def sauvegarder_regles(self, regles: ReglesMaintenance) -> None:
        """
        Sauvegarde (remplace) l'ensemble des règles pour une agence.
        """
        self.repo.save(regles)

    def appliquer_regles(self, agence_id: UUID, cout_base: Cout, duree: Duree,
                         date_intervention: date) -> Cout:
        """
        Applique les règles de tarification sur le coût de base d'une intervention.

        Args:
            agence_id: UUID de l'agence (pour récupérer ses règles)
            cout_base: coût de base (main-d'œuvre + pièces)
            duree: durée de l'intervention
            date_intervention: date de l'intervention

        Returns:
            Cout: coût final après application des règles
        """
        regles = self.repo.get(agence_id)
        if regles is None:
            return cout_base  # aucune règle, coût inchangé

        return regles.calculer_cout(cout_base, duree, date_intervention)