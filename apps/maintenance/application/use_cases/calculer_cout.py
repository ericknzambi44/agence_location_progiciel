"""
Use case pour calculer le coût d'une intervention sans la terminer.
Ce calcul n'applique pas les règles de tarification (remises, majorations, forfaits),
car celles-ci ne sont appliquées qu'à la terminaison de l'intervention.
"""
from decimal import Decimal
from uuid import UUID
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.value_objects.cout import Cout


class CalculerCoutInterventionUseCase:
    """
    Use case pour obtenir le coût estimé d'une intervention (sans terminer).
    """

    def __init__(self, repo: InterventionRepository):
        self.repo = repo

    def execute(self, intervention_id: UUID) -> Cout:
        """
        Calcule le coût de base de l'intervention (main-d'œuvre + pièces).

        Args:
            intervention_id: UUID de l'intervention

        Returns:
            Cout: coût total (sans application des règles de tarification)

        Raises:
            ValueError: si l'intervention n'existe pas
        """
        intervention = self.repo.get(intervention_id)
        if not intervention:
            raise ValueError("Intervention introuvable")

        # La méthode calculer_cout() retourne le coût total en float
        # et met à jour les attributs internes _cout_main_oeuvre et _cout_total
        cout_float = intervention.calculer_cout()
        return Cout(Decimal(str(cout_float)))