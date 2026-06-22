from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from location.domain.repositories.client_repository import ClientRepository
from location.domain.entities.client import Client
from location.infrastructure.models import ClientModel
from location.infrastructure.mappers.client_mapper import ClientMapper
from shared_kernel.domain.value_objects import Email


class DjangoClientRepository(ClientRepository):
    def get(self, id: UUID) -> Optional[Client]:
        try:
            model = ClientModel.objects.get(id=id)
            return ClientMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: Email) -> Optional[Client]:
        try:
            model = ClientModel.objects.get(email=email.value)
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

    def list_all(self) -> List[Client]:
        models = ClientModel.objects.all()
        return [ClientMapper.to_domain(m) for m in models]