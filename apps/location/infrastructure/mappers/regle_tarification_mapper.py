from uuid import UUID

from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle
from location.domain.entities.regle_tarification import ReglesTarification
from location.infrastructure.models import RegleTarificationModel
from decimal import Decimal


class RegleTarificationMapper:
    @staticmethod
    def to_domain(model: RegleTarificationModel) -> RegleTarification:
        return RegleTarification(
            type=TypeRegle(model.type),
            valeur=Decimal(str(model.valeur)),
            duree_min=model.duree_min,
            duree_max=model.duree_max,
            type_bien_id=model.type_bien_id,
            periode_debut=model.periode_debut,
            periode_fin=model.periode_fin,
            description=model.description,
            active=model.active
        )

    @staticmethod
    def to_model(agence_id: UUID, regle: RegleTarification) -> RegleTarificationModel:
        return RegleTarificationModel(
            agence_id=agence_id,
            type=regle.type.value,
            valeur=regle.valeur,
            duree_min=regle.duree_min,
            duree_max=regle.duree_max,
            type_bien_id=regle.type_bien_id,
            periode_debut=regle.periode_debut,
            periode_fin=regle.periode_fin,
            description=regle.description,
            active=regle.active
        )