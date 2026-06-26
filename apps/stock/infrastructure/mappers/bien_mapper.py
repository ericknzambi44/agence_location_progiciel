"""
Mapper pour convertir entre l'entité domaine Bien et le modèle Django BienModel.
Gère la conversion du Value Object PrixHT (montant + devise).
"""
from decimal import Decimal

from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.value_objects.prix import PrixHT
from stock.infrastructure.models import BienModel


class BienMapper:
    """
    Conversion bidirectionnelle entre l'entité Bien et le modèle ORM.
    """

    @staticmethod
    def to_domain(model: BienModel) -> Bien:
        """
        Construit une entité Bien à partir du modèle Django.

        Args:
            model (BienModel): Instance du modèle ORM.

        Returns:
            Bien: Entité domaine.
        """
        # Création du Value Object PrixHT à partir des champs du modèle
        prix_vo = PrixHT(
            amount=Decimal(str(model.prix_unitaire_ht)),
            currency=model.devise or "USD"
        )

        return Bien(
            id=model.id,
            reference=model.reference,
            nom=model.nom,
            description=model.description,
            prix_unitaire_ht=prix_vo,
            date_achat=model.date_achat,
            etat=EtatBien(model.etat)
        )

    @staticmethod
    def to_model(entity: Bien) -> BienModel:
        """
        Construit un modèle Django à partir de l'entité Bien.

        Args:
            entity (Bien): Entité domaine.

        Returns:
            BienModel: Instance du modèle ORM.
        """
        # Extraction du montant et de la devise depuis le Value Object
        return BienModel(
            id=entity.id,
            reference=entity.reference,
            nom=entity.nom,
            description=entity.description,
            prix_unitaire_ht=entity.prix_unitaire_ht.amount,
            devise=entity.prix_unitaire_ht.currency,
            date_achat=entity.date_achat,
            etat=entity.etat.value
        )