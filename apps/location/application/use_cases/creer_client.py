from uuid import UUID
from administration.domain.value_objects.telephone import Telephone
from location.domain.entities.client import Client
from location.domain.repositories.client_repository import ClientRepository
from shared_kernel.domain.value_objects import Email, PersonName



class CreerClientUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, nom: str, prenom: str, email: str, telephone: str, adresse: str, agence_id: UUID = None) -> Client:
        if agence_id is None:
            raise ValueError("agence_id est requis pour créer un client.")

        nom_vo = PersonName(nom)
        prenom_vo = PersonName(prenom)
        email_vo = Email(email)
        tel_vo = Telephone(telephone)

        # Vérifier unicité email (dans l'agence)
        if self.repo.get_by_email(email_vo, agence_id=agence_id):
            raise ValueError("Un client avec cet email existe déjà dans cette agence.")

        client = Client(
            nom=nom_vo,
            prenom=prenom_vo,
            email=email_vo,
            telephone=tel_vo,
            adresse=adresse,
            agence_id=agence_id
        )
        self.repo.add(client)
        return client