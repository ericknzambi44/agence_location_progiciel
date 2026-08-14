from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.value_objects.prix import PrixHT
from stock.infrastructure.models import Bien as BienModel

class BienMapper:
    @staticmethod
    def to_domain(model: BienModel) -> Bien:
        return Bien(
            id=model.id,
            reference=model.reference,
            nom=model.nom,
            description=model.description,
            prix_unitaire_ht=PrixHT(
                amount=model.prix_unitaire_ht,
                currency=model.devise
            ),
            date_achat=model.date_achat,
            etat=EtatBien(model.etat),
            agence_id=model.agence_id,
        )

    @staticmethod
    def to_model(entity: Bien) -> BienModel:
        return BienModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            description=entity.description,
            prix_unitaire_ht=entity.prix_unitaire_ht.amount,
            devise=entity.prix_unitaire_ht.currency,
            date_achat=entity.date_achat,
            etat=entity.etat.value,
            agence_id=entity.agence_id,
        )