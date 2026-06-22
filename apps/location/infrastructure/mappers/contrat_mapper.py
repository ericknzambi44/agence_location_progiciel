from location.domain.entities.contrat import Contrat
from location.domain.value_objects.montant import Montant
from location.infrastructure.models import ContratModel
from decimal import Decimal


class ContratMapper:
    @staticmethod
    def to_domain(model: ContratModel) -> Contrat:
        return Contrat(
            id=model.id,
            client_id=model.client_id,
            bien_id=model.bien_id,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            montant_total=Montant(model.montant_total),
            statut=model.statut
        )

    @staticmethod
    def to_model(entity: Contrat) -> ContratModel:
        return ContratModel(
            id=entity.id,
            client_id=entity.client_id,
            bien_id=entity.bien_id,
            date_debut=entity.date_debut,
            date_fin=entity.date_fin,
            montant_total=entity.montant_total.valeur,
            statut=entity.statut
        )