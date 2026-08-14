"""
Mapper Pointage : convertit entre le modèle Django `Pointage` et l'entité domaine `Pointage`.

Fait partie de la couche infrastructure (persistance).
"""

from rh.domain.entities.pointage import Pointage
from rh.infrastructure.models import Pointage as PointageModel  # alias


class PointageMapper:
    """
    Convertit les objets entre le modèle de persistance `Pointage`
    et l'entité du domaine `Pointage`.
    """

    @staticmethod
    def to_domain(model: PointageModel) -> Pointage:
        """
        Convertit une instance `PointageModel` en entité domaine.

        Args:
            model (PointageModel): Instance du modèle ORM.

        Returns:
            Pointage: Entité domaine correspondante.
        """
        return Pointage(
            id=model.id,
            employe_id=model.employe_id,
            horodatage=model.horodatage,
            type=model.type,
            commentaire=model.commentaire or "",
        )

    @staticmethod
    def to_model(entity: Pointage) -> PointageModel:
        """
        Convertit une entité domaine `Pointage` en instance du modèle Django.

        Args:
            entity (Pointage): Entité domaine à convertir.

        Returns:
            PointageModel: Instance du modèle ORM (non persistée).
        """
        return PointageModel(
            id=entity.id,
            employe_id=entity.employe_id,
            horodatage=entity.horodatage,
            type=entity.type,
            commentaire=entity.commentaire,
        )