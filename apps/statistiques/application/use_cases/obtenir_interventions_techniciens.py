from datetime import date
from typing import List, Dict, Any
from statistiques.application.services.agregation_service import AggregationService

class ObtenirInterventionsTechniciensUseCase:
    def __init__(self, service: AggregationService):
        self.service = service

    def execute(self, debut: date, fin: date) -> List[Dict[str, Any]]:
        return self.service.get_interventions_techniciens(debut, fin)