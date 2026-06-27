"""
Repository Django pour les règles de tarification de maintenance.
"""
from typing import Optional
from uuid import UUID

from maintenance.domain.repositories.regle_maintenance_repository import RegleMaintenanceRepository
from maintenance.domain.entities.regle_maintenance import ReglesMaintenance
from maintenance.infrastructure.models import RegleMaintenanceModel
from maintenance.infrastructure.mappers.regle_maintenance_mapper import RegleMaintenanceMapper


class DjangoRegleMaintenanceRepository(RegleMaintenanceRepository):
    """
    Implémentation du repository des règles de maintenance avec Django ORM.
    """

    def get(self, agence_id: UUID) -> Optional[ReglesMaintenance]:
        """
        Récupère toutes les règles de tarification pour une agence donnée.

        Args:
            agence_id: UUID de l'agence

        Returns:
            ReglesMaintenance: agrégat contenant les règles, ou None si aucune.
        """
        models = RegleMaintenanceModel.objects.filter(agence_id=agence_id)
        if not models.exists():
            return None
        regles = [RegleMaintenanceMapper.to_domain(m) for m in models]
        return ReglesMaintenance(agence_id=agence_id, regles=regles)

    def save(self, regles: ReglesMaintenance) -> None:
        """
        Sauvegarde (remplace) l'ensemble des règles pour une agence.
        Supprime les anciennes et crée les nouvelles.

        Args:
            regles: agrégat ReglesMaintenance contenant les nouvelles règles.
        """
        # Suppression des anciennes règles de l'agence
        RegleMaintenanceModel.objects.filter(agence_id=regles.agence_id).delete()

        # Création des nouvelles
        for r in regles.regles:
            model = RegleMaintenanceMapper.to_model(r)
            model.save()