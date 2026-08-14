"""
Repository Django pour les clients.

Gère la persistance des entités `Client` avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""

from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID

from location.domain.repositories.client_repository import ClientRepository
from location.domain.entities.client import Client
from location.infrastructure.models import Client  # Modèle Django (Client)
from location.infrastructure.mappers.client_mapper import ClientMapper
from shared_kernel.domain.value_objects import Email


class DjangoClientRepository(ClientRepository):
    """
    Implémentation du repository des clients avec Django ORM.
    """

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Client]:
        """
        Récupère un client par son identifiant, filtré par agence.

        Args:
            id (UUID): Identifiant du client.
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            Optional[Client]: Entité domaine si trouvée, sinon None.
        """
        try:
            qs = Client.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ClientMapper.to_domain(model)
        except Client.DoesNotExist:
            return None

    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Client]:
        """
        Récupère un client par son adresse email, filtré par agence.

        Args:
            email (Email): Value object de l'email.
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            Optional[Client]: Entité domaine si trouvée, sinon None.
        """
        try:
            qs = Client.objects.filter(email=email.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ClientMapper.to_domain(model)
        except Client.DoesNotExist:
            return None

    def add(self, client: Client) -> None:
        """
        Insère un nouveau client, en exigeant une agence.

        Args:
            client (Client): Entité domaine à persister.
        """
        if not hasattr(client, 'agence_id') or client.agence_id is None:
            raise ValueError("Le client doit avoir un agence_id pour être sauvegardé.")
        model = ClientMapper.to_model(client)
        model.save()
        client.id = model.id

    def update(self, client: Client) -> None:
        """
        Met à jour un client existant.

        Args:
            client (Client): Entité domaine avec modifications.
        """
        model = ClientMapper.to_model(client)
        model.save()

    def list_all(self, agence_id: UUID = None) -> List[Client]:
        """
        Retourne tous les clients d'une agence (liste vide si agence_id None).

        Args:
            agence_id (UUID, optionnel): Identifiant de l'agence.

        Returns:
            List[Client]: Liste des entités domaine.
        """
        if agence_id is None:
            return []  # sécurité
        models = Client.objects.filter(agence_id=agence_id)
        return [ClientMapper.to_domain(m) for m in models]