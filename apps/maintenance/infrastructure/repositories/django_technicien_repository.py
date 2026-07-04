"""
Repository Django pour les techniciens.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID

from maintenance.domain.repositories.technicien_repository import TechnicienRepository
from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import TechnicienModel
from maintenance.infrastructure.mappers.technicien_mapper import TechnicienMapper


class DjangoTechnicienRepository(TechnicienRepository):
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Technicien]:
        """
        Récupère un technicien par son ID.
        Si agence_id est fourni, vérifie qu'il appartient à cette agence.
        """
        try:
            qs = TechnicienModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return TechnicienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str, agence_id: UUID = None) -> Optional[Technicien]:
        """
        Récupère un technicien par son email.
        Si agence_id est fourni, vérifie qu'il appartient à cette agence.
        """
        try:
            qs = TechnicienModel.objects.filter(email=email)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return TechnicienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, technicien: Technicien) -> None:
        """
        Ajoute un nouveau technicien.
        L'agence_id doit déjà être défini dans l'entité.
        """
        if not hasattr(technicien, 'agence_id') or technicien.agence_id is None:
            raise ValueError("Le technicien doit avoir un agence_id pour être sauvegardé.")
        model = TechnicienMapper.to_model(technicien)
        model.save()
        technicien.id = model.id

    def update(self, technicien: Technicien) -> None:
        model = TechnicienMapper.to_model(technicien)
        model.save()

    def remove(self, technicien: Technicien) -> None:
        TechnicienModel.objects.filter(id=technicien.id).delete()

    def get_all(self, agence_id: UUID = None) -> List[Technicien]:
        """
        Retourne tous les techniciens de l'agence.
        Si agence_id est None, retourne une liste vide.
        """
        if agence_id is None:
            return []
        models = TechnicienModel.objects.filter(agence_id=agence_id)
        return [TechnicienMapper.to_domain(m) for m in models]