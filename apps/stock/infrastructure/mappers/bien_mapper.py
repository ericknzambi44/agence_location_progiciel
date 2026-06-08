from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.value_objects.reference_bien import ReferenceBien
from stock.domain.value_objects.prix import PrixHT
from stock.infrastructure.models import BienModel, CategorieModel
from .categorie_mapper import CategorieMapper

class BienMapper:
    @staticmethod
    def to_domain(model: BienModel) -> Bien:
        prix = PrixHT(amount=model.prix_unitaire_ht, currency="EUR")
        ref = ReferenceBien(model.reference)
        categorie = CategorieMapper.to_domain(model.categorie) if model.categorie else None
        return Bien(
            id=model.id,
            reference=ref.value,  # ReferenceBien est un VO, on stocke sa valeur string
            nom=model.nom,
            description=model.description,
            prix_unitaire_ht=prix.amount,  # on garde Decimal pour simplifier
            date_achat=model.date_achat,
            etat=EtatBien(model.etat),
            # catégorie à ajouter dans l'entité Bien si besoin (ajout attribut)
        )
        # Note: si on veut l'attribut catégorie dans Bien, il faut modifier l'entité.

    @staticmethod
    def to_model(entity: Bien) -> BienModel:
        return BienModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            description=entity.description,
            prix_unitaire_ht=entity.prix_unitaire_ht,
            date_achat=entity.date_achat,
            etat=entity.etat.value,
        )