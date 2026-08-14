"""
Repository Django pour les employés.

Gère la persistance des entités `Employe` avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.

Ce module implémente le port `EmployeRepository` défini dans la couche domaine.
"""

from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.entities.employe import Employe
from rh.infrastructure.models import Employe
from rh.infrastructure.mappers.employe_mapper import EmployeMapper
from shared_kernel.domain.value_objects import Email
from rh.domain.value_objects.matricule import Matricule


class DjangoEmployeRepository(EmployeRepository):
    """
    Implémentation du repository des employés avec Django ORM.

    Cette classe est responsable de :
        - Convertir les entités du domaine en modèles Django et vice-versa.
        - Assurer l'isolation par agence (toutes les requêtes de lecture
          exigent un `agence_id` non nul pour éviter les fuites inter-agences).
        - Gérer les relations ManyToMany (groupes) lors de la sauvegarde.
    """

    # --------------------------------------------------------------------------
    # Méthodes de lecture
    # --------------------------------------------------------------------------

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son identifiant unique.

        Args:
            id (UUID): Identifiant de l'employé.
            agence_id (UUID, optionnel): Si fourni, filtre pour que l'employé
                appartienne à cette agence.

        Returns:
            Optional[Employe]: L'entité domaine si trouvée, sinon None.
        """
        try:
            qs = Employe.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except Employe.DoesNotExist:
            return None

    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son adresse email.

        Args:
            email (Email): Value object de l'email.
            agence_id (UUID, optionnel): Filtre par agence si fourni.

        Returns:
            Optional[Employe]: L'entité domaine si trouvée, sinon None.
        """
        try:
            qs = Employe.objects.filter(email=email.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except Employe.DoesNotExist:
            return None

    def get_by_matricule(self, matricule: Matricule, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son matricule.

        Args:
            matricule (Matricule): Value object du matricule.
            agence_id (UUID, optionnel): Filtre par agence si fourni.

        Returns:
            Optional[Employe]: L'entité domaine si trouvée, sinon None.
        """
        try:
            qs = Employe.objects.filter(matricule=matricule.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except Employe.DoesNotExist:
            return None

    def list_all(self, agence_id: UUID = None) -> List[Employe]:
        """
        Retourne tous les employés (actifs et inactifs) d'une agence.

        Args:
            agence_id (UUID, optionnel): Identifiant de l'agence.
                Si None, retourne une liste vide (sécurité).

        Returns:
            List[Employe]: Liste des entités domaine.
        """
        if agence_id is None:
            return []

        models = Employe.objects.filter(agence_id=agence_id).order_by('matricule')
        result = []
        for model in models:
            try:
                result.append(EmployeMapper.to_domain(model))
            except Exception:
                # Ignore les employés dont le mapping échoue (données invalides)
                continue
        return result

    def list_actifs(self, agence_id: UUID = None) -> List[Employe]:
        """
        Retourne uniquement les employés actifs d'une agence.

        Args:
            agence_id (UUID, optionnel): Identifiant de l'agence.
                Si None, retourne une liste vide (sécurité).

        Returns:
            List[Employe]: Liste des entités domaine actives.
        """
        if agence_id is None:
            return []

        models = Employe.objects.filter(agence_id=agence_id, est_actif=True).order_by('matricule')
        result = []
        for model in models:
            try:
                result.append(EmployeMapper.to_domain(model))
            except Exception:
                continue
        return result

    # --------------------------------------------------------------------------
    # Méthodes d'écriture
    # --------------------------------------------------------------------------

    def add(self, employe: Employe) -> None:
        """
        Insère un nouvel employé en base de données.

        Cette méthode :
            1. Convertit l'entité domaine en modèle Django.
            2. Sauvegarde l'instance (ce qui génère l'ID si absent).
            3. Affecte les groupes (M2M) à partir de `employe.group_ids`.
            4. Met à jour l'ID de l'entité domaine avec celui généré.

        Args:
            employe (Employe): L'entité domaine à persister.
        """
        model = EmployeMapper.to_model(employe)
        model.save()

        # Gestion de la relation ManyToMany (groupes)
        if employe.group_ids:
            model.groups.set(employe.group_ids)

        # Mise à jour de l'ID de l'entité (si nouvellement créé)
        employe.id = model.id

    def update(self, employe: Employe) -> None:
        """
        Met à jour un employé existant.

        Args:
            employe (Employe): L'entité domaine avec les modifications.
        """
        model = EmployeMapper.to_model(employe)
        model.save()

        # Synchronisation des groupes
        model.groups.set(employe.group_ids)

    def save(self, employe: Employe) -> None:
        """
        Sauvegarde un employé : appelle `add` si l'ID n'existe pas encore,
        sinon `update`.

        Args:
            employe (Employe): L'entité domaine à sauvegarder.
        """
        if employe.id is None:
            self.add(employe)
        else:
            # Vérifier si l'employé existe déjà
            if self.get(employe.id, employe.agence_id) is None:
                self.add(employe)
            else:
                self.update(employe)

    def soft_delete(self, employe: Employe) -> None:
        """
        Désactive un employé (soft delete).

        L'employé n'est pas supprimé physiquement ; son attribut `est_actif`
        est mis à False. Si un utilisateur Django est lié, il est également
        désactivé.

        Args:
            employe (Employe): L'entité domaine à désactiver.
        """
        model = Employe.objects.get(id=employe.id)
        model.est_actif = False
        model.save()

        # Désactiver l'utilisateur lié si présent
        if model.user:
            model.user.is_active = False
            model.user.save()