"""
Use case pour créer un client.

Vérifie l'unicité de l'email dans l'agence,
construit l'entité Client avec les Value Objects, puis persiste.
"""

from uuid import UUID

from administration.domain.value_objects.telephone import Telephone
from location.domain.entities.client import Client
from location.domain.repositories.client_repository import ClientRepository
from shared_kernel.domain.value_objects import Email, PersonName


class CreerClientUseCase:
    """
    Use case de création d'un client.
    """

    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(
        self,
        nom: str,
        prenom: str,
        email: str,
        telephone: str,
        adresse: str,
        agence_id: UUID = None
    ) -> Client:
        """
        Exécute la création d'un client.

        Args:
            nom (str): Nom de famille.
            prenom (str): Prénom.
            email (str): Adresse email.
            telephone (str): Numéro de téléphone.
            adresse (str): Adresse postale.
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Returns:
            Client: L'entité client créée.

        Raises:
            ValueError: si l'agence est manquante, si l'email existe déjà
                        dans cette agence, ou si les données sont invalides.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour créer un client.")

        # Conversion des primitives en Value Objects
        nom_vo = PersonName(nom)
        prenom_vo = PersonName(prenom)
        email_vo = Email(email)
        tel_vo = Telephone(telephone)

        # Vérification de l'unicité de l'email (dans l'agence)
        if self.repo.get_by_email(email_vo, agence_id=agence_id):
            raise ValueError("Un client avec cet email existe déjà dans cette agence.")

        # Construction de l'entité Client
        client = Client(
            nom=nom_vo,
            prenom=prenom_vo,
            email=email_vo,
            telephone=tel_vo,
            adresse=adresse,
            agence_id=agence_id
        )

        # Persistance
        self.repo.add(client)

        return client