"""
Service d'agrégation des données statistiques.
Centralise les appels aux repositories et structure les données.
Toutes les méthodes acceptent un paramètre `agence_id` pour le filtrage multi-agences.
"""
from typing import List, Dict, Any, Optional
from datetime import date
from uuid import UUID
from statistiques.domain.repositories.statistiques_repository import StatistiquesRepository
from statistiques.domain.value_objects.periode import Periode, UnitePeriode


class AggregationService:
    """
    Service d'agrégation des données statistiques.
    """

    def __init__(self, repo: StatistiquesRepository):
        self.repo = repo

    def get_revenus(self, debut: date, fin: date,
                    unite: UnitePeriode = UnitePeriode.MOIS,
                    agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=unite)
        return self.repo.get_revenus_par_periode(periode, agence_id=agence_id)

    def get_revenus_par_bien(self, debut: date, fin: date,
                             agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_revenus_par_bien(periode, agence_id=agence_id)

    def get_revenus_par_client(self, debut: date, fin: date,
                               agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_revenus_par_client(periode, agence_id=agence_id)

    def get_contrats_par_periode(self, debut: date, fin: date,
                                 unite: UnitePeriode = UnitePeriode.MOIS,
                                 agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=unite)
        return self.repo.get_nombre_contrats_par_periode(periode, agence_id=agence_id)

    def get_contrats_par_statut(self, debut: date, fin: date,
                                agence_id: UUID = None) -> Dict[str, int]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_nombre_contrats_par_statut(periode, agence_id=agence_id)

    def get_taux_occupation_global(self, debut: date, fin: date,
                                   agence_id: UUID = None) -> float:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_taux_occupation_global(periode, agence_id=agence_id)

    def get_biens_populaires(self, debut: date, fin: date,
                             limite: int = 5,
                             agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_biens_les_plus_loues(periode, limite, agence_id=agence_id)

    def get_pieces_populaires(self, debut: date, fin: date,
                              limite: int = 5,
                              agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_pieces_les_plus_utilisees(periode, limite, agence_id=agence_id)

    def get_interventions_techniciens(self, debut: date, fin: date,
                                      agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_interventions_par_technicien(periode, agence_id=agence_id)

    def get_statistiques_interventions(self, debut: date, fin: date,
                                       agence_id: UUID = None) -> Dict[str, Any]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_statistiques_interventions(periode, agence_id=agence_id)

    def get_clients_actifs(self, debut: date, fin: date,
                           agence_id: UUID = None) -> int:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_nombre_clients_actifs(periode, agence_id=agence_id)

    def get_clients_plus_actifs(self, debut: date, fin: date,
                                limite: int = 5,
                                agence_id: UUID = None) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_clients_plus_actifs(periode, limite, agence_id=agence_id)

    def get_synthese(self, debut: date, fin: date,
                     agence_id: UUID = None) -> Dict[str, Any]:
        """
        Retourne une synthèse complète des indicateurs sur la période donnée,
        filtrée par agence.
        """
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)

        # Appels aux différentes méthodes du repository avec agence_id
        revenus = self.repo.get_revenus_par_periode(periode, agence_id=agence_id)
        contrats = self.repo.get_nombre_contrats_par_periode(periode, agence_id=agence_id)
        contrats_statut = self.repo.get_nombre_contrats_par_statut(periode, agence_id=agence_id)
        taux_occupation = self.repo.get_taux_occupation_global(periode, agence_id=agence_id)
        biens_populaires = self.repo.get_biens_les_plus_loues(periode, 5, agence_id=agence_id)
        pieces_populaires = self.repo.get_pieces_les_plus_utilisees(periode, 5, agence_id=agence_id)
        interventions_techniciens = self.repo.get_interventions_par_technicien(periode, agence_id=agence_id)
        clients_actifs = self.repo.get_nombre_clients_actifs(periode, agence_id=agence_id)
        statistiques_interventions = self.repo.get_statistiques_interventions(periode, agence_id=agence_id)

        return {
            "revenus": revenus,
            "contrats": contrats,
            "contrats_statut": contrats_statut,
            "taux_occupation": taux_occupation,
            "biens_populaires": biens_populaires,
            "pieces_populaires": pieces_populaires,
            "interventions_techniciens": interventions_techniciens,
            "clients_actifs": clients_actifs,
            "statistiques_interventions": statistiques_interventions,
        }