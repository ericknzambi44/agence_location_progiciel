from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import BienModel

class BienMapper:
    @staticmethod
    def to_domain(model: BienModel) -> Bien:
        return Bien(
            id=model.id,
            reference=model.reference,
            nom=model.nom,
            description=model.description,
            prix_unitaire_ht=model.prix_unitaire_ht,
            date_achat=model.date_achat,
            etat=EtatBien(model.etat)
        )

    @staticmethod
    def to_model(entity: Bien) -> BienModel:
        return BienModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            description=entity.description,
            prix_unitaire_ht=entity.prix_unitaire_ht,
            date_achat=entity.date_achat,
            etat=entity.etat.value
        )