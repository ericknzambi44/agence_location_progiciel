from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from typing import Optional, List
from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.entities.employe import Employe
from rh.infrastructure.models import EmployeModel
from rh.infrastructure.mappers.employe_mapper import EmployeMapper
from shared_kernel.domain.value_objects import Email
from rh.domain.value_objects.matricule import Matricule

class DjangoEmployeRepository(EmployeRepository):
    def get(self, id: UUID) -> Optional[Employe]:
        try:
            model = EmployeModel.objects.get(id=id)
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: Email) -> Optional[Employe]:
        try:
            model = EmployeModel.objects.get(email=email.value)
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_matricule(self, matricule: Matricule) -> Optional[Employe]:
        try:
            model = EmployeModel.objects.get(matricule=matricule.value)
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, employe: Employe) -> None:
        model = EmployeMapper.to_model(employe)
        model.save()
        employe.id = model.id

    def update(self, employe: Employe) -> None:
        model = EmployeMapper.to_model(employe)
        model.save()

    def list_actifs(self) -> List[Employe]:
        models = EmployeModel.objects.filter(est_actif=True)
        return [EmployeMapper.to_domain(m) for m in models]