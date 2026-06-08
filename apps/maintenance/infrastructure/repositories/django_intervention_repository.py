from django.core.exceptions import ObjectDoesNotExist
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.entities.intervention import Intervention
from maintenance.infrastructure.models import InterventionModel
from maintenance.infrastructure.mappers.intervention_mapper import InterventionMapper
from datetime import datetime
from uuid import UUID

class DjangoInterventionRepository(InterventionRepository):
    def get(self, id: UUID):
        try:
            model = InterventionModel.objects.get(id=id)
            return InterventionMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, intervention: Intervention):
        model = InterventionMapper.to_model(intervention)
        model.save()
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)
        intervention.id = model.id

    def remove(self, intervention: Intervention):
        InterventionModel.objects.filter(id=intervention.id).delete()

    def find_by_bien(self, bien_id: UUID):
        models = InterventionModel.objects.filter(bien_id=bien_id)
        return [InterventionMapper.to_domain(m) for m in models]

    def find_by_technicien(self, technicien_id: UUID):
        models = InterventionModel.objects.filter(technicien__id=technicien_id)
        return [InterventionMapper.to_domain(m) for m in models]

    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime):
        # Recherche les interventions qui chevauchent la période donnée
        conflits = InterventionModel.objects.filter(
            technicien__id=technicien_id,
            date_debut_prevue__lt=fin,
            date_fin_prevue__gt=debut
        )
        return [InterventionMapper.to_domain(c) for c in conflits]

    def find_all(self):
        return [InterventionMapper.to_domain(m) for m in InterventionModel.objects.all()]