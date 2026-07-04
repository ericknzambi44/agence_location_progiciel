from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from datetime import date
from location.domain.repositories.contrat_repository import ContratRepository
from location.domain.entities.contrat import Contrat
from location.infrastructure.models import ContratModel
from location.infrastructure.mappers.contrat_mapper import ContratMapper


class DjangoContratRepository(ContratRepository):
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Contrat]:
        try:
            qs = ContratModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ContratMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, contrat: Contrat) -> None:
        if not hasattr(contrat, 'agence_id') or contrat.agence_id is None:
            raise ValueError("Le contrat doit avoir un agence_id.")
        model = ContratMapper.to_model(contrat)
        model.save()
        contrat.id = model.id

    def update(self, contrat: Contrat) -> None:
        model = ContratMapper.to_model(contrat)
        model.save()

    def find_by_bien_et_periode(self, bien_id: UUID, debut: date, fin: date, agence_id: UUID = None) -> List[Contrat]:
        qs = ContratModel.objects.filter(
            bien_id=bien_id,
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]

    def find_by_client(self, client_id: UUID, agence_id: UUID = None) -> List[Contrat]:
        qs = ContratModel.objects.filter(client_id=client_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]

    def find_actifs(self, agence_id: UUID = None) -> List[Contrat]:
        if agence_id is None:
            return []
        qs = ContratModel.objects.filter(statut='actif', agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]