from typing import List, Dict, Any
from datetime import date
from uuid import UUID
from statistiques.domain.repositories.statistiques_repository import StatistiquesRepository
from statistiques.domain.value_objects.periode import Periode, UnitePeriode

class AggregationService:
    """
    Service d'agrégation des données statistiques.
    Centralise les appels aux repositories et structure les données.
    """
    def __init__(self, repo: StatistiquesRepository):
        self.repo = repo

    def get_revenus(self, debut: date, fin: date, unite: UnitePeriode = UnitePeriode.MOIS) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=unite)
        return self.repo.get_revenus_par_periode(periode)

    def get_revenus_par_bien(self, debut: date, fin: date) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)  # l'unité n'est pas utilisée
        return self.repo.get_revenus_par_bien(periode)

    def get_revenus_par_client(self, debut: date, fin: date) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_revenus_par_client(periode)

    def get_contrats_par_periode(self, debut: date, fin: date, unite: UnitePeriode = UnitePeriode.MOIS) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=unite)
        return self.repo.get_nombre_contrats_par_periode(periode)

    def get_contrats_par_statut(self, debut: date, fin: date) -> Dict[str, int]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)  # unité non utilisée
        return self.repo.get_nombre_contrats_par_statut(periode)

    def get_taux_occupation_global(self, debut: date, fin: date) -> float:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_taux_occupation_global(periode)

    def get_biens_populaires(self, debut: date, fin: date, limite: int = 5) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_biens_les_plus_loues(periode, limite)

    def get_pieces_populaires(self, debut: date, fin: date, limite: int = 5) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_pieces_les_plus_utilisees(periode, limite)

    def get_interventions_techniciens(self, debut: date, fin: date) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_interventions_par_technicien(periode)

    def get_statistiques_interventions(self, debut: date, fin: date) -> Dict[str, Any]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_statistiques_interventions(periode)

    def get_clients_actifs(self, debut: date, fin: date) -> int:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_nombre_clients_actifs(periode)

    def get_clients_plus_actifs(self, debut: date, fin: date, limite: int = 5) -> List[Dict[str, Any]]:
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)
        return self.repo.get_clients_plus_actifs(periode, limite)

    def get_synthese(self, debut: date, fin: date) -> Dict[str, Any]:
        """
        Retourne une synthèse complète des indicateurs sur la période donnée.
        """
        periode = Periode(debut=debut, fin=fin, unite=UnitePeriode.MOIS)

        # Appels aux différentes méthodes du repository
        revenus = self.repo.get_revenus_par_periode(periode)
        contrats = self.repo.get_nombre_contrats_par_periode(periode)
        contrats_statut = self.repo.get_nombre_contrats_par_statut(periode)
        taux_occupation = self.repo.get_taux_occupation_global(periode)
        biens_populaires = self.repo.get_biens_les_plus_loues(periode, 5)
        pieces_populaires = self.repo.get_pieces_les_plus_utilisees(periode, 5)
        interventions_techniciens = self.repo.get_interventions_par_technicien(periode)
        clients_actifs = self.repo.get_nombre_clients_actifs(periode)
        statistiques_interventions = self.repo.get_statistiques_interventions(periode)

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