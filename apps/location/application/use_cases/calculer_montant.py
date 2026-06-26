"""
Use case pour calculer le montant estimé d'une location.
Utilise le service de tarification pour appliquer les règles (remises, forfaits, majorations)
en fonction du bien, de sa catégorie, de la durée et de la période.
"""
from datetime import date
from uuid import UUID
from decimal import Decimal

from location.domain.value_objects.montant import Montant
from stock.domain.repositories.bien_repository import BienRepository
from location.application.services.tarification_service import TarificationService


class CalculerMontantLocationUseCase:
    """
    Use case pour estimer le montant total d'une location avant création du contrat.
    """

    def __init__(self, bien_repo: BienRepository, tarif_service: TarificationService):
        self.bien_repo = bien_repo
        self.tarif_service = tarif_service

    def execute(self, bien_id: UUID, agence_id: UUID, date_debut: date, date_fin: date) -> Montant:
        """
        Exécute le calcul du montant estimé.

        Args:
            bien_id: UUID du bien
            agence_id: UUID de l'agence (pour les règles)
            date_debut: date de début de la location
            date_fin: date de fin de la location

        Returns:
            Montant: montant total estimé

        Raises:
            ValueError: si bien introuvable, dates invalides ou durée nulle.
        """
        # Récupération du bien
        bien = self.bien_repo.get(bien_id)
        if not bien:
            raise ValueError("Bien introuvable")

        # Validation des dates
        if date_debut >= date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")
        jours = (date_fin - date_debut).days
        if jours <= 0:
            raise ValueError("La durée de location doit être d'au moins un jour.")

        # Récupération du prix unitaire depuis le Value Object PrixHT
        prix_base = bien.prix_unitaire_ht.amount  # Decimal

        # Récupération de la catégorie du bien (si présente)
        categorie_id = getattr(bien, 'categorie_id', None)

        # Calcul du prix final via le service de tarification
        prix_final = self.tarif_service.calculer_prix(
            agence_id=agence_id,
            prix_base=prix_base,
            duree=jours,
            bien_id=bien_id,
            categorie_id=categorie_id,
            date_debut=date_debut
        )

        return Montant(prix_final)