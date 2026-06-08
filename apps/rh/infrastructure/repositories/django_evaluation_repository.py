from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from rh.domain.repositories.evaluation_repository import EvaluationRepository
from rh.domain.entities.evaluation import Evaluation
from rh.infrastructure.models import EvaluationModel
from rh.infrastructure.mappers.evaluation_mapper import EvaluationMapper

class DjangoEvaluationRepository(EvaluationRepository):
    def add(self, evaluation: Evaluation) -> None:
        model = EvaluationMapper.to_model(evaluation)
        model.save()
        evaluation.id = model.id

    def get(self, id: UUID) -> Optional[Evaluation]:
        try:
            model = EvaluationModel.objects.get(id=id)
            return EvaluationMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_last_for_employe(self, employe_id: UUID, limit: int = 1) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(employe_id=employe_id).order_by('-date_evaluation')[:limit]
        return [EvaluationMapper.to_domain(m) for m in models]

    def list_for_employe(self, employe_id: UUID) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(employe_id=employe_id).order_by('-date_evaluation')
        return [EvaluationMapper.to_domain(m) for m in models]

    def update(self, evaluation: Evaluation) -> None:
        model = EvaluationMapper.to_model(evaluation)
        model.save()