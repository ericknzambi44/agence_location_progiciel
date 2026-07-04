"""
Implémentation concrète du repository pour les pièces détachées avec Django ORM.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID

from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import PieceDetacheeModel
from maintenance.infrastructure.mappers.piece_mapper import PieceDetacheeMapper


class DjangoPieceDetacheeRepository(PieceDetacheeRepository):
    """Repository Django pour les pièces détachées."""

    def get(self, piece_id: UUID, agence_id: UUID = None) -> Optional[PieceDetachee]:
        """
        Récupère une pièce par son ID.
        Si agence_id est fourni, vérifie que la pièce appartient à cette agence.
        """
        try:
            qs = PieceDetacheeModel.objects.filter(id=piece_id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return PieceDetacheeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def find_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[PieceDetachee]:
        """
        Recherche une pièce par sa référence.
        Si agence_id est fourni, la référence doit appartenir à cette agence.
        """
        try:
            qs = PieceDetacheeModel.objects.filter(reference=reference)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return PieceDetacheeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    # Alias pour compatibilité (appelé par certains use cases)
    def get_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[PieceDetachee]:
        return self.find_by_reference(reference, agence_id)

    def add(self, piece: PieceDetachee) -> None:
        """
        Ajoute une nouvelle pièce.
        L'agence_id doit déjà être défini dans l'entité.
        """
        if not hasattr(piece, 'agence_id') or piece.agence_id is None:
            raise ValueError("La pièce doit avoir un agence_id pour être sauvegardée.")
        model = PieceDetacheeMapper.to_model(piece)
        model.save()
        piece.id = model.id

    def update(self, piece: PieceDetachee) -> None:
        model = PieceDetacheeMapper.to_model(piece)
        model.save()

    def remove(self, piece: PieceDetachee) -> None:
        PieceDetacheeModel.objects.filter(id=piece.id).delete()

    def find_all(self, agence_id: UUID = None) -> List[PieceDetachee]:
        """
        Retourne toutes les pièces de l'agence.
        Si agence_id est None, retourne une liste vide.
        """
        if agence_id is None:
            return []
        models = PieceDetacheeModel.objects.filter(agence_id=agence_id)
        return [PieceDetacheeMapper.to_domain(m) for m in models]