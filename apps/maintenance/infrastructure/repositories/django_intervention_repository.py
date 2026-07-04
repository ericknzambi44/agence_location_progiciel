"""
Repository Django pour les interventions de maintenance.
Gère la persistance des entités Intervention avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist

from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.entities.intervention import Intervention
from maintenance.infrastructure.models import InterventionModel
from maintenance.infrastructure.mappers.intervention_mapper import InterventionMapper
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository


class DjangoInterventionRepository(InterventionRepository):
    def __init__(self):
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Intervention]:
        """
        Récupère une intervention par son ID.
        Si agence_id est fourni, vérifie que l'intervention appartient à cette agence.
        """
        try:
            qs = InterventionModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return InterventionMapper.to_domain(model, self.technicien_repo, self.piece_repo)
        except ObjectDoesNotExist:
            return None

    def add(self, intervention: Intervention) -> None:
        """
        Ajoute une nouvelle intervention.
        L'agence_id doit déjà être défini dans l'entité (ou être passé via le mapper).
        """
        # Vérification que l'entité a un agence_id
        if not hasattr(intervention, 'agence_id') or intervention.agence_id is None:
            raise ValueError("L'intervention doit avoir un agence_id pour être sauvegardée.")

        intervention.id = None
        model = InterventionMapper.to_model(intervention)
        model.save()
        intervention.id = model.id
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def update(self, intervention: Intervention) -> None:
        if intervention.id is None:
            raise ValueError("ID requis pour mise à jour")
        # On ne filtre pas par agence_id ici car on utilise déjà l'ID
        model = InterventionModel.objects.get(id=intervention.id)
        model.bien_id = intervention.bien_id
        model.technicien_id = intervention.technicien.id if intervention.technicien else None
        model.date_debut = intervention.date_debut
        model.date_fin = intervention.date_fin
        model.statut = intervention.statut
        model.cout_main_oeuvre = intervention._cout_main_oeuvre
        model.cout_total = intervention._cout_total
        model.save(update_fields=[
            'bien_id', 'technicien_id', 'date_debut', 'date_fin',
            'statut', 'cout_main_oeuvre', 'cout_total'
        ])
        model.pieces.all().delete()
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def remove(self, intervention: Intervention) -> None:
        InterventionModel.objects.filter(id=intervention.id).delete()

    def find_by_bien(self, bien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        qs = InterventionModel.objects.filter(bien_id=bien_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_by_technicien(self, technicien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        qs = InterventionModel.objects.filter(technicien_id=technicien_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_by_periode(self, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        qs = InterventionModel.objects.filter(
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        qs = InterventionModel.objects.filter(
            technicien_id=technicien_id,
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_all(self, agence_id: UUID = None) -> List[Intervention]:
        """
        Retourne toutes les interventions de l'agence.
        Si agence_id est None, retourne une liste vide (sauf superuser).
        """
        if agence_id is None:
            return []  # Sécurité : on ne renvoie rien si agence_id non spécifié
        qs = InterventionModel.objects.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]