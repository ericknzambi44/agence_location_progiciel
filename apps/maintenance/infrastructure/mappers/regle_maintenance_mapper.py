"""
Mapper pour la conversion entre le modèle Django RegleMaintenance et l'entité domaine RegleMaintenance.
"""

from decimal import Decimal

from maintenance.domain.entities.regle_maintenance import RegleMaintenance
from maintenance.domain.value_objects.regle_maintenance import TypeRegleMaintenance
from maintenance.infrastructure.models import RegleMaintenance as RegleMaintenanceModel  # alias


class RegleMaintenanceMapper:
    """
    Convertit une règle de tarification de maintenance entre le domaine et l'infrastructure.
    """

    @staticmethod
    def to_domain(model: RegleMaintenanceModel) -> RegleMaintenance:
        """
        Construit une entité domaine à partir du modèle Django.

        Args:
            model (RegleMaintenanceModel): Instance du modèle ORM.

        Returns:
            RegleMaintenance: Entité domaine.
        """
        return RegleMaintenance(
            type=TypeRegleMaintenance(model.type),
            valeur=Decimal(str(model.valeur)),
            agence_id=model.agence_id,
            duree_min=model.duree_min,
            duree_max=model.duree_max,
            periode_debut=model.periode_debut,
            periode_fin=model.periode_fin,
            description=model.description,
            active=model.active
        )

    @staticmethod
    def to_model(regle: RegleMaintenance) -> RegleMaintenanceModel:
        """
        Construit un modèle Django à partir de l'entité domaine.

        Args:
            regle (RegleMaintenance): Entité domaine.

        Returns:
            RegleMaintenanceModel: Instance ORM prête à être sauvegardée.
        """
        return RegleMaintenanceModel(
            agence_id=regle.agence_id,
            type=regle.type.value,
            valeur=regle.valeur,
            duree_min=regle.duree_min,
            duree_max=regle.duree_max,
            periode_debut=regle.periode_debut,
            periode_fin=regle.periode_fin,
            description=regle.description,
            active=regle.active
        )