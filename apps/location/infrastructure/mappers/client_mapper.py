"""
Mapper entre l'entité domaine Client et le modèle ORM Client.

Assure la conversion bidirectionnelle, incluant l'agence_id pour le multi-agences.
"""

from administration.domain.value_objects.telephone import Telephone
from location.domain.entities.client import Client
from location.infrastructure.models import Client as ClientModel  # alias pour cohérence
from shared_kernel.domain.value_objects import Email, PersonName


class ClientMapper:
    """
    Conversion bidirectionnelle pour les clients.
    """

    @staticmethod
    def to_domain(model: ClientModel) -> Client:
        """
        Construit une entité Client à partir du modèle Django.

        Args:
            model (ClientModel): Instance du modèle ORM.

        Returns:
            Client: Entité domaine.
        """
        return Client(
            id=model.id,
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            telephone=Telephone(model.telephone),
            adresse=model.adresse,
            agence_id=model.agence_id,
            est_actif=model.est_actif
        )

    @staticmethod
    def to_model(entity: Client) -> ClientModel:
        """
        Construit un modèle Django à partir de l'entité Client.

        Args:
            entity (Client): Entité domaine.

        Returns:
            ClientModel: Instance ORM non persistée.
        """
        return ClientModel(
            id=entity.id,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            telephone=entity.telephone.value,
            adresse=entity.adresse,
            agence_id=entity.agence_id,
            est_actif=entity.est_actif
        )