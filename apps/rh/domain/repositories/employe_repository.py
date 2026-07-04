"""
Repository abstrait pour l'entité Employe.
Définit les opérations de persistance avec support du filtrage par agence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from rh.domain.entities.employe import Employe
from rh.domain.value_objects.matricule import Matricule
from shared_kernel.domain.value_objects import Email


class EmployeRepository(ABC):
    """
    Interface pour la persistance des employés.
    Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
    """

    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son ID.
        Si agence_id est fourni, l'employé doit appartenir à cette agence.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: Email, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son email.
        Si agence_id est fourni, l'employé doit appartenir à cette agence.
        """
        pass

    @abstractmethod
    def get_by_matricule(self, matricule: Matricule, agence_id: UUID = None) -> Optional[Employe]:
        """
        Récupère un employé par son matricule.
        Si agence_id est fourni, l'employé doit appartenir à cette agence.
        """
        pass

    @abstractmethod
    def add(self, employe: Employe) -> None:
        """
        Ajoute un nouvel employé (l'agence_id doit déjà être défini dans l'entité).
        """
        pass

    @abstractmethod
    def update(self, employe: Employe) -> None:
        """
        Met à jour un employé existant.
        """
        pass

    @abstractmethod
    def list_actifs(self, agence_id: UUID = None) -> List[Employe]:
        """
        Retourne la liste des employés actifs.
        Si agence_id est fourni, filtre par agence.
        """
        pass