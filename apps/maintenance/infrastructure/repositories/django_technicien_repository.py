"""
Repository Django pour les techniciens.

Toutes les méthodes de lecture supportent le filtrage par agence.
"""

from typing import Optional, List
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import Technicien  # Modèle Django (Technicien)
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper


class DjangoTechnicienRepository(TechnicienRepository):
    """
    Implémentation du repository des techniciens avec Django ORM.
    """

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Technicien]:
        """
        Récupère un technicien par son identifiant, filtré par agence.
        """
        try:
            qs = Technicien.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return TechnicienMapper.to_domain(model)
        except Technicien.DoesNotExist:
            return None

    def get_by_email(self, email: str, agence_id: UUID = None) -> Optional[Technicien]:
        """
        Récupère un technicien par son email, filtré par agence.
        """
        try:
            qs = Technicien.objects.filter(email=email)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return TechnicienMapper.to_domain(model)
        except Technicien.DoesNotExist:
            return None

    def add(self, technicien: Technicien) -> None:
        """
        Insère un nouveau technicien, en exigeant une agence.
        """
        if not hasattr(technicien, 'agence_id') or technicien.agence_id is None:
            raise ValueError("Le technicien doit avoir un agence_id pour être sauvegardé.")
        model = TechnicienMapper.to_model(technicien)
        model.save()
        technicien.id = model.id

    def update(self, technicien: Technicien) -> None:
        """Met à jour un technicien existant."""
        model = TechnicienMapper.to_model(technicien)
        model.save()

    def remove(self, technicien: Technicien) -> None:
        """Supprime un technicien."""
        Technicien.objects.filter(id=technicien.id).delete()

    def get_all(self, agence_id: UUID = None) -> List[Technicien]:
        """
        Retourne tous les techniciens d'une agence (liste vide si pas d'agence).
        """
        if agence_id is None:
            return []
        models = Technicien.objects.filter(agence_id=agence_id)
        return [TechnicienMapper.to_domain(m) for m in models]