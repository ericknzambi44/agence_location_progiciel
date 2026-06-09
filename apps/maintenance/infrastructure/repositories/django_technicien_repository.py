from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import TechnicienModel
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper

class DjangoTechnicienRepository(TechnicienRepository):
    def get(self, id: UUID) -> Optional[Technicien]:
        try:
            model = TechnicienModel.objects.get(id=id)
            return TechnicienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, technicien: Technicien) -> None:
        model = TechnicienMapper.to_model(technicien)
        model.save()
        technicien.id = model.id

    def update(self, technicien: Technicien) -> None:
        model = TechnicienMapper.to_model(technicien)
        model.save()

    def remove(self, technicien: Technicien) -> None:
        TechnicienModel.objects.filter(id=technicien.id).delete()

    def get_all(self) -> List[Technicien]:
        models = TechnicienModel.objects.all()
        return [TechnicienMapper.to_domain(m) for m in models]