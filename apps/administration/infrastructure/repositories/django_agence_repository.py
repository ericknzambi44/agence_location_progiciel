from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from administration.domain.repositories.agence_repository import AgenceRepository
from administration.domain.entities.agence import Agence
from administration.domain.value_objects.code_agence import CodeAgence
from administration.infrastructure.models import AgenceModel
from administration.infrastructure.mappers.agence_mapper import AgenceMapper

class DjangoAgenceRepository(AgenceRepository):
    def get(self, id: UUID) -> Optional[Agence]:
        try:
            model = AgenceModel.objects.get(id=id)
            return AgenceMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_code(self, code: CodeAgence) -> Optional[Agence]:
        try:
            model = AgenceModel.objects.get(code=code.value)
            return AgenceMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_nom(self, nom: str) -> Optional[Agence]:
        try:
            model = AgenceModel.objects.get(nom=nom)
            return AgenceMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, agence: Agence) -> None:
        model = AgenceMapper.to_model(agence)
        model.save()
        agence.id = model.id

    def update(self, agence: Agence) -> None:
        model = AgenceMapper.to_model(agence)
        model.save()

    def list_actives(self) -> List[Agence]:
        models = AgenceModel.objects.filter(actif=True)
        return [AgenceMapper.to_domain(m) for m in models]

    def list_all(self) -> List[Agence]:
        models = AgenceModel.objects.all()
        return [AgenceMapper.to_domain(m) for m in models]