"""
Repository Django pour les rôles métier.

Gère la persistance des entités `Role` avec conversion via le mapper.
Implémente le port `RoleRepository` défini dans la couche domaine.
"""

from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rh.domain.repositories.role_repository import RoleRepository
from rh.domain.entities.role import Role
from rh.infrastructure.models import Role as RoleModel  # alias pour cohérence
from rh.infrastructure.mappers.role_mapper import RoleMapper


class DjangoRoleRepository(RoleRepository):
    """
    Implémentation du repository des rôles avec Django ORM.

    Cette classe est responsable de :
        - Convertir les entités du domaine en modèles Django et vice-versa.
        - Fournir les opérations CRUD de base pour les rôles.
        - Proposer des méthodes de recherche par nom.
    """

    def get(self, id: UUID) -> Optional[Role]:
        """
        Récupère un rôle par son identifiant unique.

        Args:
            id (UUID): Identifiant du rôle.

        Returns:
            Optional[Role]: L'entité domaine si trouvée, sinon None.
        """
        try:
            model = RoleModel.objects.get(id=id)
            return RoleMapper.to_domain(model)
        except RoleModel.DoesNotExist:
            return None

    def get_by_nom(self, nom: str) -> Optional[Role]:
        """
        Récupère un rôle par son nom exact.

        Args:
            nom (str): Nom du rôle.

        Returns:
            Optional[Role]: L'entité domaine si trouvée, sinon None.
        """
        try:
            model = RoleModel.objects.get(nom=nom)
            return RoleMapper.to_domain(model)
        except RoleModel.DoesNotExist:
            return None

    def add(self, role: Role) -> None:
        """
        Insère un nouveau rôle en base de données.

        Args:
            role (Role): L'entité domaine à persister.

        Note:
            L'ID de l'entité est mis à jour après la sauvegarde.
        """
        model = RoleMapper.to_model(role)
        model.save()
        role.id = model.id

    def update(self, role: Role) -> None:
        """
        Met à jour un rôle existant.

        Args:
            role (Role): L'entité domaine avec les modifications.
        """
        model = RoleMapper.to_model(role)
        model.save()

    def list_all(self) -> List[Role]:
        """
        Retourne tous les rôles métier.

        Returns:
            List[Role]: Liste des entités domaine (peut être vide).
        """
        models = RoleModel.objects.all()
        return [RoleMapper.to_domain(m) for m in models]