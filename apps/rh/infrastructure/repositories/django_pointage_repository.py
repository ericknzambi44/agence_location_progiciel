"""
Repository Django pour les pointages.

Gère la persistance des entités `Pointage` avec conversion via le mapper.
Implémente le port `PointageRepository` défini dans la couche domaine.
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rh.domain.repositories.pointage_repository import PointageRepository
from rh.domain.entities.pointage import Pointage
from rh.infrastructure.models import Pointage as PointageModel
from rh.infrastructure.mappers.pointage_mapper import PointageMapper


class DjangoPointageRepository(PointageRepository):
    """
    Implémentation du repository des pointages avec Django ORM.

    Cette classe est responsable de :
        - Convertir les entités du domaine en modèles Django et vice-versa.
        - Fournir des méthodes de recherche par employé et par date.
        - Récupérer le pointage le plus récent d'un employé.
    """

    def add(self, pointage: Pointage) -> None:
        """
        Insère un nouveau pointage en base de données.

        Args:
            pointage (Pointage): L'entité domaine à persister.

        Note:
            L'ID de l'entité est mis à jour après la sauvegarde.
        """
        model = PointageMapper.to_model(pointage)
        model.save()
        pointage.id = model.id

    def get_by_employe_and_date(self, employe_id: UUID, jour: date) -> List[Pointage]:
        """
        Retourne tous les pointages d'un employé pour une journée donnée.

        Args:
            employe_id (UUID): Identifiant de l'employé.
            jour (date): Date pour laquelle on veut les pointages.

        Returns:
            List[Pointage]: Liste des entités domaine, triées par horodatage croissant.
        """
        start = datetime.combine(jour, datetime.min.time())
        end = datetime.combine(jour, datetime.max.time())

        models = PointageModel.objects.filter(
            employe_id=employe_id,
            horodatage__range=(start, end)
        ).order_by('horodatage')

        return [PointageMapper.to_domain(m) for m in models]

    def get_dernier_pointage(self, employe_id: UUID) -> Optional[Pointage]:
        """
        Récupère le pointage le plus récent d'un employé.

        Args:
            employe_id (UUID): Identifiant de l'employé.

        Returns:
            Optional[Pointage]: Le dernier pointage si trouvé, sinon None.
        """
        try:
            model = PointageModel.objects.filter(
                employe_id=employe_id
            ).latest('horodatage')
            return PointageMapper.to_domain(model)
        except PointageModel.DoesNotExist:
            return None