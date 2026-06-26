"""
Mapper pour la conversion entre l'entité domaine RegleTarification et le modèle Django RegleTarificationModel.
Gère les nouveaux champs bien_id et categorie_id.
"""
from uuid import UUID
from decimal import Decimal

from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle
from location.domain.entities.regle_tarification import ReglesTarification
from location.infrastructure.models import RegleTarificationModel


class RegleTarificationMapper:
    """
    Convertit une règle de tarification entre le domaine et l'infrastructure.
    """

    @staticmethod
    def to_domain(model: RegleTarificationModel) -> RegleTarification:
        """
        Construit une entité domaine à partir du modèle Django.

        Args:
            model: instance de RegleTarificationModel

        Returns:
            RegleTarification: entité domaine
        """
        return RegleTarification(
            type=TypeRegle(model.type),
            valeur=Decimal(str(model.valeur)),
            duree_min=model.duree_min,
            duree_max=model.duree_max,
            bien_id=model.bien_id,      
            categorie_id=model.categorie_id,  
            periode_debut=model.periode_debut,
            periode_fin=model.periode_fin,
            description=model.description,
            active=model.active
        )

    @staticmethod
    def to_model(agence_id: UUID, regle: RegleTarification) -> RegleTarificationModel:
        """
        Construit un modèle Django à partir de l'entité domaine.

        Args:
            agence_id: UUID de l'agence propriétaire
            regle: entité RegleTarification

        Returns:
            RegleTarificationModel: instance prête à être sauvegardée
        """
        return RegleTarificationModel(
            agence_id=agence_id,
            type=regle.type.value,
            valeur=regle.valeur,
            duree_min=regle.duree_min,
            duree_max=regle.duree_max,
            bien_id=regle.bien_id,         
            categorie_id=regle.categorie_id,  
            periode_debut=regle.periode_debut,
            periode_fin=regle.periode_fin,
            description=regle.description,
            active=regle.active
        )