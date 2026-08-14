"""
Repository Django pour les évaluations.

Gère la persistance des entités `Evaluation` avec conversion via le mapper.
Implémente le port `EvaluationRepository` défini dans la couche domaine.
"""

from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rh.domain.repositories.evaluation_repository import EvaluationRepository
from rh.domain.entities.evaluation import Evaluation
from rh.infrastructure.models import Evaluation  # Modèle Django (Evaluation)
from rh.infrastructure.mappers.evaluation_mapper import EvaluationMapper


class DjangoEvaluationRepository(EvaluationRepository):
    """
    Implémentation du repository des évaluations avec Django ORM.

    Cette classe est responsable de :
        - Convertir les entités du domaine en modèles Django et vice-versa.
        - Fournir les opérations CRUD de base pour les évaluations.
        - Proposer des méthodes de recherche spécifiques (par employé, dernières évaluations).
    """

    def add(self, evaluation: Evaluation) -> None:
        """
        Insère une nouvelle évaluation en base de données.

        Args:
            evaluation (Evaluation): L'entité domaine à persister.

        Note:
            L'ID de l'entité est mis à jour après la sauvegarde.
        """
        model = EvaluationMapper.to_model(evaluation)
        model.save()
        evaluation.id = model.id

    def get(self, id: UUID) -> Optional[Evaluation]:
        """
        Récupère une évaluation par son identifiant unique.

        Args:
            id (UUID): Identifiant de l'évaluation.

        Returns:
            Optional[Evaluation]: L'entité domaine si trouvée, sinon None.
        """
        try:
            model = Evaluation.objects.get(id=id)
            return EvaluationMapper.to_domain(model)
        except Evaluation.DoesNotExist:
            return None

    def get_last_for_employe(self, employe_id: UUID, limit: int = 1) -> List[Evaluation]:
        """
        Retourne les dernières évaluations d'un employé, triées par date décroissante.

        Args:
            employe_id (UUID): Identifiant de l'employé.
            limit (int, optionnel): Nombre maximal d'évaluations à retourner.
                Par défaut : 1 (la plus récente).

        Returns:
            List[Evaluation]: Liste des entités domaine (peut être vide).
        """
        models = Evaluation.objects.filter(
            employe_id=employe_id
        ).order_by('-date_evaluation')[:limit]
        return [EvaluationMapper.to_domain(m) for m in models]

    def list_for_employe(self, employe_id: UUID) -> List[Evaluation]:
        """
        Retourne toutes les évaluations d'un employé, triées par date décroissante.

        Args:
            employe_id (UUID): Identifiant de l'employé.

        Returns:
            List[Evaluation]: Liste des entités domaine (peut être vide).
        """
        models = Evaluation.objects.filter(
            employe_id=employe_id
        ).order_by('-date_evaluation')
        return [EvaluationMapper.to_domain(m) for m in models]

    def update(self, evaluation: Evaluation) -> None:
        """
        Met à jour une évaluation existante.

        Args:
            evaluation (Evaluation): L'entité domaine avec les modifications.
        """
        model = EvaluationMapper.to_model(evaluation)
        model.save()