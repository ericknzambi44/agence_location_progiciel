from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import date
from uuid import UUID
from statistiques.domain.value_objects.periode import Periode

class StatistiquesRepository(ABC):
    """
    Interface pour récupérer les données statistiques agrégées.
    """

    @abstractmethod
    def get_revenus_par_periode(self, periode: Periode) -> List[Dict[str, Any]]:
        """Revenus (montant total) par période (jour, mois, année)."""
        pass

    @abstractmethod
    def get_revenus_par_bien(self, periode: Periode) -> List[Dict[str, Any]]:
        """Revenus par bien sur une période."""
        pass

    @abstractmethod
    def get_revenus_par_client(self, periode: Periode) -> List[Dict[str, Any]]:
        """Revenus par client sur une période."""
        pass

    @abstractmethod
    def get_nombre_contrats_par_periode(self, periode: Periode) -> List[Dict[str, Any]]:
        """Nombre de contrats par période."""
        pass

    @abstractmethod
    def get_nombre_contrats_par_statut(self, periode: Periode) -> Dict[str, int]:
        """Nombre de contrats par statut (actif, termine, annule)."""
        pass

    @abstractmethod
    def get_taux_occupation_global(self, periode: Periode) -> float:
        """Taux d'occupation global (contrats actifs / biens disponibles)."""
        pass

    @abstractmethod
    def get_taux_occupation_par_bien(self, bien_id: UUID, periode: Periode) -> float:
        """Taux d'occupation d'un bien spécifique."""
        pass

    @abstractmethod
    def get_biens_les_plus_loues(self, periode: Periode, limite: int = 5) -> List[Dict[str, Any]]:
        """Biens les plus loués en termes de nombre de contrats."""
        pass

    @abstractmethod
    def get_pieces_les_plus_utilisees(self, periode: Periode, limite: int = 5) -> List[Dict[str, Any]]:
        """Pièces détachées les plus utilisées (quantité totale, coût total)."""
        pass

    @abstractmethod
    def get_interventions_par_technicien(self, periode: Periode) -> List[Dict[str, Any]]:
        """Performances des techniciens : nombre, coût total, durée moyenne."""
        pass

    @abstractmethod
    def get_statistiques_interventions(self, periode: Periode) -> Dict[str, Any]:
        """Statistiques globales sur les interventions (nombre, durée moyenne, min, max, écart-type)."""
        pass

    @abstractmethod
    def get_clients_plus_actifs(self, periode: Periode, limite: int = 5) -> List[Dict[str, Any]]:
        """Clients ayant le plus de contrats ou le plus de dépenses."""
        pass

    @abstractmethod
    def get_nombre_clients_actifs(self, periode: Periode) -> int:
        """Nombre de clients ayant au moins un contrat sur la période."""
        pass