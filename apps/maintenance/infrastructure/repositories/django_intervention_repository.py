from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.entities.intervention import Intervention
from maintenance.infrastructure.models import InterventionModel
from maintenance.infrastructure.mappers.intervention_mapper import InterventionMapper

class DjangoInterventionRepository(InterventionRepository):
    def get(self, intervention_id: UUID) -> Optional[Intervention]:
        try:
            model = InterventionModel.objects.get(id=intervention_id)
            return InterventionMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, intervention: Intervention) -> None:
        model = InterventionMapper.to_model(intervention, include_id=False)
        # Force la génération d'un nouvel ID par la base de données
        model.id = None
        model.save()
        intervention.id = model.id

    def update(self, intervention: Intervention) -> None:
        model = InterventionMapper.to_model(intervention, include_id=True)
        model.save(force_update=True)

    def remove(self, intervention: Intervention) -> None:
        InterventionModel.objects.filter(id=intervention.id).delete()

    def find_all(self) -> List[Intervention]:
        models = InterventionModel.objects.all()
        return [InterventionMapper.to_domain(m) for m in models]

    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime) -> List[Intervention]:
        conflits = InterventionModel.objects.filter(
            technicien_id=technicien_id,
            statut__in=['planifiee', 'en_cours'],
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        return [InterventionMapper.to_domain(c) for c in conflits]

    def find_by_bien(self, bien_id: UUID) -> List[Intervention]:
        models = InterventionModel.objects.filter(bien_id=bien_id)
        return [InterventionMapper.to_domain(m) for m in models]

    def find_by_technicien(self, technicien_id: UUID) -> List[Intervention]:
        models = InterventionModel.objects.filter(technicien_id=technicien_id)
        return [InterventionMapper.to_domain(m) for m in models]