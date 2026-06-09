from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import PieceDetacheeModel
from maintenance.infrastructure.mappers.piece_mapper import PieceDetacheeMapper

class DjangoPieceDetacheeRepository(PieceDetacheeRepository):
    def get(self, piece_id: UUID) -> Optional[PieceDetachee]:
        try:
            model = PieceDetacheeModel.objects.get(id=piece_id)
            return PieceDetacheeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_reference(self, reference: str) -> Optional[PieceDetachee]:
        return self.find_by_reference(reference)

    def find_by_reference(self, reference: str) -> Optional[PieceDetachee]:
        try:
            model = PieceDetacheeModel.objects.get(reference=reference)
            return PieceDetacheeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, piece: PieceDetachee) -> None:
        model = PieceDetacheeMapper.to_model(piece)
        model.save()
        piece.id = model.id

    def update(self, piece: PieceDetachee) -> None:
        model = PieceDetacheeMapper.to_model(piece)
        model.save()

    def remove(self, piece: PieceDetachee) -> None:
        PieceDetacheeModel.objects.filter(id=piece.id).delete()

    def find_all(self) -> List[PieceDetachee]:
        models = PieceDetacheeModel.objects.all()
        return [PieceDetacheeMapper.to_domain(m) for m in models]