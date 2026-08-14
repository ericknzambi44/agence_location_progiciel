"""
Mapper entre l'entité domaine Contrat et le modèle ORM Contrat.

Assure la conversion bidirectionnelle, incluant l'agence_id pour le multi-agences.
"""

from location.domain.entities.contrat import Contrat
from location.domain.value_objects.montant import Montant
from location.infrastructure.models import Contrat as ContratModel  # alias


class ContratMapper:
    """
    Conversion bidirectionnelle pour les contrats.
    """

    @staticmethod
    def to_domain(model: ContratModel) -> Contrat:
        """
        Construit une entité Contrat à partir du modèle Django.

        Args:
            model (ContratModel): Instance du modèle ORM.

        Returns:
            Contrat: Entité domaine.
        """
        return Contrat(
            id=model.id,
            client_id=model.client_id,
            bien_id=model.bien_id,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            montant_total=Montant(model.montant_total),
            statut=model.statut,
            agence_id=model.agence_id
        )

    @staticmethod
    def to_model(entity: Contrat) -> ContratModel:
        """
        Construit un modèle Django à partir de l'entité Contrat.

        Args:
            entity (Contrat): Entité domaine.

        Returns:
            ContratModel: Instance ORM non persistée.
        """
        return ContratModel(
            id=entity.id,
            client_id=entity.client_id,
            bien_id=entity.bien_id,
            date_debut=entity.date_debut,
            date_fin=entity.date_fin,
            montant_total=entity.montant_total.valeur,
            statut=entity.statut,
            agence_id=entity.agence_id
        )