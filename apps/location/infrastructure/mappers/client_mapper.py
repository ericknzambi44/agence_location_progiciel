from administration.domain.value_objects.telephone import Telephone
from location.domain.entities.client import Client
from location.infrastructure.models import ClientModel
from shared_kernel.domain.value_objects import Email, PersonName



class ClientMapper:
    @staticmethod
    def to_domain(model: ClientModel) -> Client:
        return Client(
            id=model.id,
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            telephone=Telephone(model.telephone),
            adresse=model.adresse,
            est_actif=model.est_actif
        )

    @staticmethod
    def to_model(entity: Client) -> ClientModel:
        return ClientModel(
            id=entity.id,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            telephone=entity.telephone.value,
            adresse=entity.adresse,
            est_actif=entity.est_actif
        )