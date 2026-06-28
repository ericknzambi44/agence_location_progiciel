from datetime import date

from statistiques.application.services.agregation_service import AggregationService
 

class ObtenirStatistiquesGeneralesUseCase:
    def __init__(self, service: AggregationService):
        self.service = service

    def execute(self, date_debut: date, date_fin: date) -> dict:
        return self.service.get_overview(date_debut, date_fin)