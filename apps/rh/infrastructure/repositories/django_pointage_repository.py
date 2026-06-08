from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from rh.domain.repositories.pointage_repository import PointageRepository
from rh.domain.entities.pointage import Pointage
from rh.infrastructure.models import PointageModel
from rh.infrastructure.mappers.pointage_mapper import PointageMapper

class DjangoPointageRepository(PointageRepository):
    def add(self, pointage: Pointage) -> None:
        model = PointageMapper.to_model(pointage)
        model.save()
        pointage.id = model.id

    def get_by_employe_and_date(self, employe_id: UUID, jour: date) -> List[Pointage]:
        start = datetime.combine(jour, datetime.min.time())
        end = datetime.combine(jour, datetime.max.time())
        models = PointageModel.objects.filter(
            employe_id=employe_id,
            horodatage__range=(start, end)
        ).order_by('horodatage')
        return [PointageMapper.to_domain(m) for m in models]

    def get_dernier_pointage(self, employe_id: UUID) -> Optional[Pointage]:
        try:
            model = PointageModel.objects.filter(employe_id=employe_id).latest('horodatage')
            return PointageMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None