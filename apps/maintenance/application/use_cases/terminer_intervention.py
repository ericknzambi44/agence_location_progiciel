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
    def __init__(self,
                 repo: InterventionRepository,
                 tarif_service: TarificationMaintenanceService):
        self.repo = repo
        self.tarif_service = tarif_service

    def execute(self, intervention_id: UUID, agence_id: UUID, date_intervention: date) -> float:
        """
        Termine l'intervention et applique les règles de tarification.

        Args:
            intervention_id: UUID de l'intervention
            agence_id: UUID de l'agence (pour les règles)
            date_intervention: date de l'intervention (pour les règles avec période)

        Returns:
            float: coût total final
        """
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")

        # Calcul du coût de base (main-d'œuvre + pièces)
        # La méthode calculer_cout() retourne le coût total en float
        # et met à jour _cout_main_oeuvre et _cout_total
        cout_base_float = intervention.calculer_cout()
        cout_base = Cout(intervention._cout_main_oeuvre + sum(
            Decimal(str(piece.prix_unitaire)) * quantite
            for piece, quantite in intervention.pieces_utilisees
        ))  # On reconstruit le coût de base (sans règles)
        # Mais on peut aussi utiliser les attributs déjà calculés.
        # Pour éviter de recalculer, on peut créer un objet Cout à partir de _cout_main_oeuvre + cout_pieces.

        # Récupération de la durée
        if not intervention.date_debut or not intervention.date_fin:
            raise ValueError("Les dates de l'intervention ne sont pas définies")
        duree_heures = (intervention.date_fin - intervention.date_debut).total_seconds() / 3600
        duree = Duree(duree_heures)

        # Application des règles
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