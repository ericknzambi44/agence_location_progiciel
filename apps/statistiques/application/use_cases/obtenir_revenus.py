from datetime import date
from typing import List, Dict, Any
from statistiques.domain.value_objects.periode import UnitePeriode
from statistiques.application.services.agregation_service import AggregationService

class ObtenirRevenusUseCase:
    def __init__(self, service: AggregationService):
        self.service = service

    def execute(self, debut: date, fin: date, unite: UnitePeriode = UnitePeriode.MOIS) -> List[Dict[str, Any]]:
        return self.service.get_revenus(debut, fin, unite)