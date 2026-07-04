"""
Repository Django pour les employés.
Gère la persistance des entités Employe avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.
"""
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from typing import Optional, List
from rh.domain.repositories.employe_repository import EmployeRepository
from rh.domain.entities.employe import Employe
from rh.infrastructure.models import EmployeModel
from rh.infrastructure.mappers.employe_mapper import EmployeMapper
from shared_kernel.domain.value_objects import Email
from rh.domain.value_objects.matricule import Matricule
import traceback


class DjangoEmployeRepository(EmployeRepository):
    """
    Implémentation du repository des employés avec Django ORM.
    """

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son ID.
        Si agence_id est fourni, vérifie que l'employé appartient à cette agence.
        """
        try:
            qs = EmployeModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son email.
        Si agence_id est fourni, vérifie que l'employé appartient à cette agence.
        """
        try:
            qs = EmployeModel.objects.filter(email=email.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_matricule(self, matricule: Matricule, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son matricule.
        Si agence_id est fourni, vérifie que l'employé appartient à cette agence.
        """
        try:
            qs = EmployeModel.objects.filter(matricule=matricule.value)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return EmployeMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, employe: Employe) -> None:
        """
        Ajoute un nouvel employé.
        L'agence_id doit déjà être défini dans l'entité.
        """
        model = EmployeMapper.to_model(employe)
        model.save()
        employe.id = model.id

    def update(self, employe: Employe) -> None:
        """
        Met à jour un employé existant.
        """
        model = EmployeMapper.to_model(employe)
        model.save()

    def list_actifs(self, agence_id: UUID = None) -> List[Employe]:
        """
        Retourne la liste des employés actifs.
        Si agence_id est fourni, filtre par agence.
        Si agence_id est None, retourne une liste vide (sauf pour les superusers, géré dans le ViewSet).
        """
        if agence_id is None:
            return []  # Sécurité : on ne renvoie rien si agence_id non spécifié

        models = EmployeModel.objects.filter(est_actif=True, agence_id=agence_id)
        result = []
        for m in models:
            try:
                result.append(EmployeMapper.to_domain(m))
            except Exception as e:
                print(f"Erreur sur l'employé {m.id} (matricule {m.matricule}): {e}")
                traceback.print_exc()
                # On ignore l'employé problématique pour l'instant
        return result