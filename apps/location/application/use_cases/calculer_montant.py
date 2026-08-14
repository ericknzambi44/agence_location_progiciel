"""
Use case pour calculer le montant estimé d'une location.

Utilise le service de tarification pour appliquer les règles (remises, forfaits,
majorations) en fonction du bien, de sa catégorie, de la durée et de la période.
Le bien doit appartenir à l'agence spécifiée.
"""

from datetime import date
from uuid import UUID

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

    def execute(
        self,
        bien_id: UUID,
        agence_id: UUID,
        date_debut: date,
        date_fin: date
    ) -> Montant:
        """
        Exécute le calcul du montant estimé.

        Args:
            bien_id (UUID): Identifiant du bien.
            agence_id (UUID): Identifiant de l'agence (pour les règles et le filtrage).
            date_debut (date): Date de début de la location.
            date_fin (date): Date de fin de la location.

        Returns:
            Montant: Montant total estimé.

        Raises:
            ValueError: si bien introuvable, dates invalides, durée nulle,
                        ou agence non spécifiée.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour calculer le montant.")

        # Récupération du bien avec filtrage par agence
        bien = self.bien_repo.get(bien_id, agence_id=agence_id)
        if not bien:
            raise ValueError("Bien introuvable ou non autorisé pour votre agence.")

        # Validation des dates
        if date_debut >= date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin.")
        jours = (date_fin - date_debut).days
        if jours <= 0:
            raise ValueError("La durée de location doit être d'au moins un jour.")

        # Récupération du prix unitaire depuis le Value Object PrixHT
        prix_base = bien.prix_unitaire_ht.amount

        # Récupération de la catégorie du bien (si présente)
        # L'entité Bien possède un attribut `categorie_id` ou `categorie.id` selon le mapping.
        # Ici on utilise `categorie_id` directement s'il existe, sinon on l'obtient
        # à partir de `categorie` si celle-ci est une entité.
        categorie_id = getattr(bien, 'categorie_id', None)
        if categorie_id is None and hasattr(bien, 'categorie') and bien.categorie:
            categorie_id = bien.categorie.id

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