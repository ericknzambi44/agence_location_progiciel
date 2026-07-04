from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from location.domain.repositories.client_repository import ClientRepository
from location.domain.entities.client import Client
from location.infrastructure.models import ClientModel
from location.infrastructure.mappers.client_mapper import ClientMapper
from shared_kernel.domain.value_objects import Email


class DjangoClientRepository(ClientRepository):
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Client]:
        try:
            qs = ClientModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ClientMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Client]:
        try:
            qs = ClientModel.objects.filter(email=email.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ClientMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, client: Client) -> None:
        model = ClientMapper.to_model(client)
        model.save()
        client.id = model.id

    def update(self, client: Client) -> None:
        model = ClientMapper.to_model(client)
        model.save()

    def list_all(self, agence_id: UUID = None) -> List[Client]:
        if agence_id is None:
            return []  # sécurité
        models = ClientModel.objects.filter(agence_id=agence_id)
        return [ClientMapper.to_domain(m) for m in models]