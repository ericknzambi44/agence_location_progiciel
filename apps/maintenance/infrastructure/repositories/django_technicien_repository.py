from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from maintenance.infrastructure.models import TechnicienModel
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper

class DjangoTechnicienRepository(TechnicienRepository):
    def get(self, id):
        try:
            model = TechnicienModel.objects.get(id=id)
            return TechnicienMapper.to_domain(model)
        except TechnicienModel.DoesNotExist:
            return None

    def get_all(self):
        return [TechnicienMapper.to_domain(m) for m in TechnicienModel.objects.all()]