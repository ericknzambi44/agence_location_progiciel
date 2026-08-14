"""
Repository Django pour les interventions de maintenance.

Gère la persistance des entités `Intervention` avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from maintenance.domain.repositories.intervention_repository import InterventionRepository
from maintenance.domain.entities.intervention import Intervention
from maintenance.infrastructure.models import Intervention  # Modèle Django (Intervention)
from maintenance.infrastructure.mappers.intervention_mapper import InterventionMapper
from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.infrastructure.repositories.django_piece_detachee_repository import DjangoPieceDetacheeRepository


class DjangoInterventionRepository(InterventionRepository):
    """
    Implémentation du repository des interventions avec Django ORM.
    """

    def __init__(self):
        self.technicien_repo = DjangoTechnicienRepository()
        self.piece_repo = DjangoPieceDetacheeRepository()

    # --------------------------------------------------------------------------
    # Lecture
    # --------------------------------------------------------------------------

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Intervention]:
        """
        Récupère une intervention par son identifiant, en filtrant par agence.
        """
        try:
            qs = Intervention.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return InterventionMapper.to_domain(model, self.technicien_repo, self.piece_repo)
        except Intervention.DoesNotExist:
            return None

    def find_by_bien(self, bien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        """Retourne les interventions liées à un bien donné, filtrées par agence."""
        qs = Intervention.objects.filter(bien_id=bien_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_by_technicien(self, technicien_id: UUID, agence_id: UUID = None) -> List[Intervention]:
        """Retourne les interventions assignées à un technicien, filtrées par agence."""
        qs = Intervention.objects.filter(technicien_id=technicien_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_by_periode(self, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        """Retourne les interventions planifiées/en cours sur une période, filtrées par agence."""
        qs = Intervention.objects.filter(
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_conflits(self, technicien_id: UUID, debut: datetime, fin: datetime, agence_id: UUID = None) -> List[Intervention]:
        """Retourne les interventions conflictuelles pour un technicien sur une période."""
        qs = Intervention.objects.filter(
            technicien_id=technicien_id,
            date_debut__lt=fin,
            date_fin__gt=debut,
            statut__in=['planifiee', 'en_cours']
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    def find_all(self, agence_id: UUID = None) -> List[Intervention]:
        """Retourne toutes les interventions d'une agence (liste vide si pas d'agence)."""
        if agence_id is None:
            return []
        qs = Intervention.objects.filter(agence_id=agence_id)
        return [InterventionMapper.to_domain(m, self.technicien_repo, self.piece_repo) for m in qs]

    # --------------------------------------------------------------------------
    # Écriture
    # --------------------------------------------------------------------------

    def add(self, intervention: Intervention) -> None:
        """
        Insère une nouvelle intervention, en exigeant une agence.

        Args:
            intervention (Intervention): Entité domaine à persister.
        """
        if not hasattr(intervention, 'agence_id') or intervention.agence_id is None:
            raise ValueError("L'intervention doit avoir un agence_id pour être sauvegardée.")

        intervention.id = None  # Le modèle générera un UUID
        model = InterventionMapper.to_model(intervention)
        model.save()
        intervention.id = model.id

        # Sauvegarde des pièces associées
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def update(self, intervention: Intervention) -> None:
        """
        Met à jour une intervention existante, y compris ses pièces.

        Args:
            intervention (Intervention): Entité domaine avec modifications.
        """
        if intervention.id is None:
            raise ValueError("ID requis pour mise à jour.")

        model = Intervention.objects.get(id=intervention.id)
        model.bien_id = intervention.bien_id
        model.technicien_id = intervention.technicien.id if intervention.technicien else None
        model.date_debut = intervention.date_debut
        model.date_fin = intervention.date_fin
        model.statut = intervention.statut
        model.cout_main_oeuvre = getattr(intervention, '_cout_main_oeuvre', 0)
        model.cout_total = getattr(intervention, '_cout_total', 0)
        model.save(update_fields=[
            'bien_id', 'technicien_id', 'date_debut', 'date_fin',
            'statut', 'cout_main_oeuvre', 'cout_total'
        ])

        # Remplacement des pièces
        model.pieces.all().delete()
        InterventionMapper.save_pieces(model, intervention.pieces_utilisees)

    def remove(self, intervention: Intervention) -> None:
        """
        Supprime définitivement une intervention.

        Args:
            intervention (Intervention): Entité à supprimer.
        """
        Intervention.objects.filter(id=intervention.id).delete()