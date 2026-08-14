"""
Repository Django pour les contrats.

Gère la persistance des entités `Contrat` avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""

from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from datetime import date

from location.domain.repositories.contrat_repository import ContratRepository
from location.domain.entities.contrat import Contrat
from location.infrastructure.models import Contrat  # Modèle Django (Contrat)
from location.infrastructure.mappers.contrat_mapper import ContratMapper


class DjangoContratRepository(ContratRepository):
    """
    Implémentation du repository des contrats avec Django ORM.
    """

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Contrat]:
        """
        Récupère un contrat par son identifiant, filtré par agence.
        """
        try:
            qs = Contrat.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return ContratMapper.to_domain(model)
        except Contrat.DoesNotExist:
            return None

    def add(self, contrat: Contrat) -> None:
        """
        Insère un nouveau contrat, en exigeant une agence.

        Args:
            contrat (Contrat): Entité domaine à persister.
        """
        if not hasattr(contrat, 'agence_id') or contrat.agence_id is None:
            raise ValueError("Le contrat doit avoir un agence_id pour être sauvegardé.")
        model = ContratMapper.to_model(contrat)
        model.save()
        contrat.id = model.id

    def update(self, contrat: Contrat) -> None:
        """
        Met à jour un contrat existant.
        """
        model = ContratMapper.to_model(contrat)
        model.save()

    def find_by_bien_et_periode(
        self,
        bien_id: UUID,
        debut: date,
        fin: date,
        agence_id: UUID = None
    ) -> List[Contrat]:
        """
        Retourne les contrats actifs chevauchant la période pour un bien donné.

        Args:
            bien_id (UUID): Identifiant du bien.
            debut (date): Début de la période.
            fin (date): Fin de la période.
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            List[Contrat]: Liste des contrats conflictuels.
        """
        qs = Contrat.objects.filter(
            bien_id=bien_id,
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]

    def find_by_client(self, client_id: UUID, agence_id: UUID = None) -> List[Contrat]:
        """
        Retourne tous les contrats d'un client, filtrés par agence.
        """
        qs = Contrat.objects.filter(client_id=client_id)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]

    def find_actifs(self, agence_id: UUID = None) -> List[Contrat]:
        """
        Retourne tous les contrats actifs d'une agence (liste vide si pas d'agence).
        """
        if agence_id is None:
            return []
        qs = Contrat.objects.filter(statut='actif', agence_id=agence_id)
        return [ContratMapper.to_domain(m) for m in qs]