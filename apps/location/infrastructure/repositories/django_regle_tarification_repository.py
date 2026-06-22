from django.core.exceptions import ObjectDoesNotExist
from typing import Optional
from uuid import UUID
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository
from location.domain.entities.regle_tarification import ReglesTarification
from location.infrastructure.models import RegleTarificationModel
from location.infrastructure.mappers.regle_tarification_mapper import RegleTarificationMapper


class DjangoRegleTarificationRepository(RegleTarificationRepository):
    def get(self, agence_id: UUID) -> Optional[ReglesTarification]:
        models = RegleTarificationModel.objects.filter(agence_id=agence_id)
        if not models.exists():
            return None
        regles = [RegleTarificationMapper.to_domain(m) for m in models]
        return ReglesTarification(agence_id=agence_id, regles=regles)

    def save(self, regles: ReglesTarification) -> None:
        # Supprimer les anciennes règles
        RegleTarificationModel.objects.filter(agence_id=regles.agence_id).delete()
        # Créer les nouvelles
        for r in regles.regles:
            model = RegleTarificationMapper.to_model(regles.agence_id, r)
            model.save()