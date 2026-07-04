"""
Repository abstrait pour l'entité Bien.
Définit les opérations de persistance avec support du filtrage par agence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import date
from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.value_objects.reference_bien import ReferenceBien


class BienRepository(ABC):
    """
    Interface pour la persistance des biens.
    Toutes les méthodes de lecture acceptent un paramètre `agence_id` pour le filtrage multi-agences.
    """

    @abstractmethod
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Bien]:
        """
        Récupère un bien par son ID.
        Si agence_id est fourni, le bien doit appartenir à cette agence.
        """
        pass

    @abstractmethod
    def get_by_reference(self, ref: ReferenceBien, agence_id: UUID = None) -> Optional[Bien]:
        """
        Récupère un bien par sa référence.
        Si agence_id est fourni, la référence doit appartenir à cette agence.
        """
        pass

    @abstractmethod
    def add(self, bien: Bien) -> None:
        """
        Ajoute un nouveau bien (l'agence_id doit déjà être défini dans l'entité).
        """
        pass

    @abstractmethod
    def update(self, bien: Bien) -> None:
        """
        Met à jour un bien existant.
        """
        pass

    @abstractmethod
    def remove(self, bien: Bien) -> None:
        """
        Supprime un bien.
        """
        pass

    @abstractmethod
    def find_by_etat(self, etat: EtatBien, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne les biens d'un état donné.
        Si agence_id est fourni, filtre par agence.
        """
        pass

    @abstractmethod
    def find_disponibles_periode(self, debut: date, fin: date, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne les biens disponibles sur une période donnée (pas de contrat actif, ni en maintenance).
        Si agence_id est fourni, filtre par agence.
        """
        pass

    @abstractmethod
    def find_all(self, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne tous les biens.
        Si agence_id est fourni, filtre par agence.
        Si agence_id est None, retourne une liste vide (sauf pour les superusers, géré dans le ViewSet).
        """
        pass