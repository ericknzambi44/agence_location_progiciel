from datetime import date
from typing import List, Dict, Any
from statistiques.application.services.agregation_service import AggregationService

class ObtenirPiecesPopulairesUseCase:
    def __init__(self, service: AggregationService):
        self.service = service

    def execute(self, debut: date, fin: date, limite: int = 5) -> List[Dict[str, Any]]:
        return self.service.get_pieces_populaires(debut, fin, limite)