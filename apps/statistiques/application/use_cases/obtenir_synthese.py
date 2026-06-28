from datetime import date
from statistiques.application.services.agregation_service import AggregationService
from statistiques.domain.value_objects.periode import UnitePeriode

class ObtenirSyntheseUseCase:
    def __init__(self, service: AggregationService):
        self.service = service

    def execute(self, debut: date, fin: date) -> dict:
        return {
            "revenus": self.service.get_revenus(debut, fin, UnitePeriode.MOIS),
            "contrats": self.service.get_contrats_par_periode(debut, fin, UnitePeriode.MOIS),
            "contrats_statut": self.service.get_contrats_par_statut(debut, fin),
            "taux_occupation": self.service.get_taux_occupation_global(debut, fin),
            "biens_populaires": self.service.get_biens_populaires(debut, fin, 5),
            "pieces_populaires": self.service.get_pieces_populaires(debut, fin, 5),
            "interventions_techniciens": self.service.get_interventions_techniciens(debut, fin),
            "clients_actifs": self.service.get_clients_actifs(debut, fin),
            "statistiques_interventions": self.service.get_statistiques_interventions(debut, fin),
        }