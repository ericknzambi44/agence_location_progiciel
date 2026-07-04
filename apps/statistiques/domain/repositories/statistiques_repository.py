"""
Repository abstrait pour les statistiques.
Toutes les méthodes acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import date
from uuid import UUID
from statistiques.domain.value_objects.periode import Periode


class StatistiquesRepository(ABC):
    @abstractmethod
    def get_revenus_par_periode(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_revenus_par_bien(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_revenus_par_client(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_nombre_contrats_par_periode(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_nombre_contrats_par_statut(self, periode: Periode, agence_id: UUID = None) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_taux_occupation_global(self, periode: Periode, agence_id: UUID = None) -> float:
        pass

    @abstractmethod
    def get_taux_occupation_par_bien(self, bien_id: UUID, periode: Periode, agence_id: UUID = None) -> float:
        pass

    @abstractmethod
    def get_biens_les_plus_loues(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_pieces_les_plus_utilisees(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_interventions_par_technicien(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_statistiques_interventions(self, periode: Periode, agence_id: UUID = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_nombre_clients_actifs(self, periode: Periode, agence_id: UUID = None) -> int:
        pass

    @abstractmethod
    def get_clients_plus_actifs(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        pass