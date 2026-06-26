"""
Repository Django pour les règles de tarification.
Utilise le mapper pour convertir entre les modèles et les entités du domaine.
"""
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional
from uuid import UUID

from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository
from location.domain.entities.regle_tarification import ReglesTarification
from location.infrastructure.models import RegleTarificationModel
from location.infrastructure.mappers.regle_tarification_mapper import RegleTarificationMapper


class DjangoRegleTarificationRepository(RegleTarificationRepository):
    """
    Implémentation du repository des règles de tarification avec Django ORM.
    """

    def get(self, agence_id: UUID) -> Optional[ReglesTarification]:
        """
        Récupère toutes les règles de tarification pour une agence donnée.

        Args:
            agence_id: UUID de l'agence

        Returns:
            ReglesTarification: agrégat contenant les règles, ou None si aucune
        """
        models = RegleTarificationModel.objects.filter(agence_id=agence_id)
        if not models.exists():
            return None
        regles = [RegleTarificationMapper.to_domain(m) for m in models]
        return ReglesTarification(agence_id=agence_id, regles=regles)

    def save(self, regles: ReglesTarification) -> None:
        """
        Sauvegarde (remplace) l'ensemble des règles pour une agence.
        Supprime les anciennes et crée les nouvelles.

        Args:
            regles: agrégat ReglesTarification contenant les nouvelles règles
        """
        # Suppression des anciennes règles de l'agence
        RegleTarificationModel.objects.filter(agence_id=regles.agence_id).delete()

        # Création des nouvelles
        for r in regles.regles:
            model = RegleTarificationMapper.to_model(regles.agence_id, r)
            model.save()