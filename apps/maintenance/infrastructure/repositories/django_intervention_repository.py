from datetime import datetime
from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.entities.intervention import Intervention
from maintenance.infrastructure.models import InterventionModel
from maintenance.infrastructure.mappers.intervention_mapper import InterventionMapper
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository

class DjangoInterventionRepository(InterventionRepository):
    def __init__(self):
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()

    def get(self, id: UUID) -> Optional[Intervention]:
        try:
            model = InterventionModel.objects.get(id=id)
            return InterventionMapper.to_domain(model, self.technicien_repo, self.piece_repo)
        except ObjectDoesNotExist:
            return None

    def add(self, intervention: Intervention) -> None:
        intervention.id = None
        model = InterventionMapper.to_model(intervention)
        model.save()
        intervention.id = model.id
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def update(self, intervention: Intervention) -> None:
        if intervention.id is None:
            raise ValueError("ID requis pour mise à jour")
        model = InterventionModel.objects.get(id=intervention.id)
        model.bien_id = intervention.bien_id
        model.technicien_id = intervention.technicien.id if intervention.technicien else None
        model.date_debut = intervention.date_debut
        model.date_fin = intervention.date_fin
        model.statut = intervention.statut
        model.cout_main_oeuvre = intervention._cout_main_oeuvre
        model.cout_total = intervention._cout_total
        model.save(update_fields=[
            'bien_id', 'technicien_id', 'date_debut', 'date_fin',
            'statut', 'cout_main_oeuvre', 'cout_total'
        ])
        model.pieces.all().delete()
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def remove(self, intervention: Intervention) -> None:
        InterventionModel.objects.filter(id=intervention.id).delete()

    def find_by_bien(self, bien_id: UUID) -> List[Intervention]:
        models = InterventionModel.objects.filter(bien_id=bien_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in models]

    def find_by_technicien(self, technicien_id: UUID) -> List[Intervention]:
        models = InterventionModel.objects.filter(technicien_id=technicien_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in models]

    def find_by_periode(self, debut: datetime, fin: datetime) -> List[Intervention]:
        # Seules les interventions actives (planifiées ou en cours) génèrent des conflits
        models = InterventionModel.objects.filter(
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in models]

    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime) -> List[Intervention]:
        models = InterventionModel.objects.filter(
            technicien_id=technicien_id,
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in models]

    def find_all(self) -> List[Intervention]:
        models = InterventionModel.objects.all()
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in models]