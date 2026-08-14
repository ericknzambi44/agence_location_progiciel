"""
Implémentation concrète du repository pour les pièces détachées avec Django ORM.

Toutes les méthodes de lecture supportent le filtrage par agence.
"""

from typing import Optional, List
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from maintenance.domain.repositories.piece_repository import PieceDetacheeRepository
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.models import PieceDetachee  # Modèle Django (PieceDetachee)
from maintenance.infrastructure.mappers.piece_detachee_mapper import PieceDetacheeMapper


class DjangoPieceDetacheeRepository(PieceDetacheeRepository):
    """
    Repository Django pour les pièces détachées.
    """

    def get(self, piece_id: UUID, agence_id: UUID = None) -> Optional[PieceDetachee]:
        """
        Récupère une pièce par son identifiant, filtrée par agence.

        Args:
            piece_id (UUID): Identifiant de la pièce.
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            Optional[PieceDetachee]: Entité domaine si trouvée, sinon None.
        """
        try:
            qs = PieceDetachee.objects.filter(id=piece_id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return PieceDetacheeMapper.to_domain(model)
        except PieceDetachee.DoesNotExist:
            return None

    def find_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[PieceDetachee]:
        """
        Recherche une pièce par sa référence, filtrée par agence.
        """
        try:
            qs = PieceDetachee.objects.filter(reference=reference)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return PieceDetacheeMapper.to_domain(model)
        except PieceDetachee.DoesNotExist:
            return None

    def get_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[PieceDetachee]:
        """Alias de `find_by_reference` pour compatibilité."""
        return self.find_by_reference(reference, agence_id)

    def add(self, piece: PieceDetachee) -> None:
        """
        Insère une nouvelle pièce, en exigeant une agence.

        Args:
            piece (PieceDetachee): Entité domaine à persister.
        """
        if not hasattr(piece, 'agence_id') or piece.agence_id is None:
            raise ValueError("La pièce doit avoir un agence_id pour être sauvegardée.")
        model = PieceDetacheeMapper.to_model(piece)
        model.save()
        piece.id = model.id

    def update(self, piece: PieceDetachee) -> None:
        """Met à jour une pièce existante."""
        model = PieceDetacheeMapper.to_model(piece)
        model.save()

    def remove(self, piece: PieceDetachee) -> None:
        """Supprime une pièce."""
        PieceDetachee.objects.filter(id=piece.id).delete()

    def find_all(self, agence_id: UUID = None) -> List[PieceDetachee]:
        """
        Retourne toutes les pièces d'une agence (liste vide si pas d'agence).
        """
        if agence_id is None:
            return []
        models = PieceDetachee.objects.filter(agence_id=agence_id)
        return [PieceDetacheeMapper.to_domain(m) for m in models]