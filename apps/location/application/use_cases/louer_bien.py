from datetime import date
from uuid import UUID
from decimal import Decimal
from location.domain.entities.contrat import Contrat
from location.domain.value_objects.montant import Montant
from location.domain.repositories.contrat_repository import ContratRepository
from location.domain.repositories.client_repository import ClientRepository
from stock.domain.repositories.bien_repository import BienRepository
from location.application.services.tarification_service import TarificationService


class LouerBienUseCase:
    def __init__(self, contrat_repo: ContratRepository, client_repo: ClientRepository,
                 bien_repo: BienRepository, tarif_service: TarificationService):
        self.contrat_repo = contrat_repo
        self.client_repo = client_repo
        self.bien_repo = bien_repo
        self.tarif_service = tarif_service

    def execute(self, client_id: UUID, bien_id: UUID, agence_id: UUID,
                date_debut: date, date_fin: date) -> Contrat:
        client = self.client_repo.get(client_id)
        if not client:
            raise ValueError("Client introuvable")
        bien = self.bien_repo.get(bien_id)
        if not bien:
            raise ValueError("Bien introuvable")

        # Vérification disponibilité
        conflits = self.contrat_repo.find_by_bien_et_periode(bien_id, date_debut, date_fin)
        if conflits:
            raise ValueError("Bien non disponible")

        jours = (date_fin - date_debut).days
        if jours <= 0:
            raise ValueError("Durée invalide")

        prix_base = Decimal(str(bien.prix_unitaire_ht).replace(',', '.'))
        prix_final = self.tarif_service.calculer_prix(agence_id, prix_base, jours, bien_id, date_debut)

        contrat = Contrat(
            client_id=client_id,
            bien_id=bien_id,
            date_debut=date_debut,
            date_fin=date_fin,
            montant_total=Montant(prix_final)
        )
        self.contrat_repo.add(contrat)
        return contrat