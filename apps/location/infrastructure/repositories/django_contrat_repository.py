from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from datetime import date
from location.domain.repositories.contrat_repository import ContratRepository
from location.domain.entities.contrat import Contrat
from location.infrastructure.models import ContratModel
from location.infrastructure.mappers.contrat_mapper import ContratMapper


class DjangoContratRepository(ContratRepository):
    def get(self, id: UUID) -> Optional[Contrat]:
        try:
            model = ContratModel.objects.get(id=id)
            return ContratMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, contrat: Contrat) -> None:
        model = ContratMapper.to_model(contrat)
        model.save()
        contrat.id = model.id

    def update(self, contrat: Contrat) -> None:
        """Met à jour un contrat existant en utilisant update_or_create."""
        model = ContratMapper.to_model(contrat)
        obj, created = ContratModel.objects.update_or_create(
            id=model.id,
            defaults={
                'client_id': model.client_id,
                'bien_id': model.bien_id,
                'date_debut': model.date_debut,
                'date_fin': model.date_fin,
                'montant_total': model.montant_total,
                'statut': model.statut,
            }
        )
        if created:
            contrat.id = obj.id

    def find_by_bien_et_periode(self, bien_id: UUID, debut: date, fin: date) -> List[Contrat]:
        models = ContratModel.objects.filter(
            bien_id=bien_id,
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        return [ContratMapper.to_domain(m) for m in models]

    def find_by_client(self, client_id: UUID) -> List[Contrat]:
        models = ContratModel.objects.filter(client_id=client_id)
        return [ContratMapper.to_domain(m) for m in models]

    def find_actifs(self) -> List[Contrat]:
        models = ContratModel.objects.filter(statut='actif')
        return [ContratMapper.to_domain(m) for m in models]