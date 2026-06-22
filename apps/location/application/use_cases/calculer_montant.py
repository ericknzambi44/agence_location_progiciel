from datetime import date
from uuid import UUID
from decimal import Decimal
from location.domain.value_objects.montant import Montant
from stock.domain.repositories.bien_repository import BienRepository
from location.application.services.tarification_service import TarificationService


class CalculerMontantLocationUseCase:
    def __init__(self, bien_repo: BienRepository, tarif_service: TarificationService):
        self.bien_repo = bien_repo
        self.tarif_service = tarif_service

    def execute(self, bien_id: UUID, agence_id: UUID, date_debut: date, date_fin: date) -> Montant:
        bien = self.bien_repo.get(bien_id)
        if not bien:
            raise ValueError("Bien introuvable")
        if date_debut >= date_fin:
            raise ValueError("date_debut < date_fin")
        jours = (date_fin - date_debut).days
        if jours <= 0:
            raise ValueError("Durée invalide")

        prix_base = Decimal(str(bien.prix_unitaire_ht).replace(',', '.'))
        prix_final = self.tarif_service.calculer_prix(agence_id, prix_base, jours, bien_id, date_debut)
        return Montant(prix_final)