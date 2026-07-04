"""
Use case pour créer un contrat de location.
Calcule le montant total en appliquant les règles de tarification,
vérifie la disponibilité du bien (état + contrats actifs), et persiste le contrat.
Toutes les vérifications tiennent compte de l'agence.
"""
from datetime import date
from uuid import UUID
from decimal import Decimal

from location.domain.entities.contrat import Contrat
from location.domain.value_objects.montant import Montant
from location.domain.repositories.contrat_repository import ContratRepository
from location.domain.repositories.client_repository import ClientRepository
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import EtatBien
from location.application.services.tarification_service import TarificationService


class LouerBienUseCase:
    """
    Use case pour louer un bien : création d'un contrat avec calcul automatique du prix.
    """

    def __init__(self, contrat_repo: ContratRepository, client_repo: ClientRepository,
                 bien_repo: BienRepository, tarif_service: TarificationService):
        self.contrat_repo = contrat_repo
        self.client_repo = client_repo
        self.bien_repo = bien_repo
        self.tarif_service = tarif_service

    def execute(self, client_id: UUID, bien_id: UUID, agence_id: UUID,
                date_debut: date, date_fin: date) -> Contrat:
        """
        Exécute la location.

        Args:
            client_id: UUID du client
            bien_id: UUID du bien
            agence_id: UUID de l'agence (pour les règles et la vérification d'appartenance)
            date_debut: date de début de la location
            date_fin: date de fin de la location

        Returns:
            Contrat: le contrat créé avec le montant total calculé

        Raises:
            ValueError: si client/bien introuvable ou non autorisé,
                        bien non disponible, dates invalides, ou erreur de tarification.
        """
        # 1. Vérification du client (avec appartenance à l'agence)
        client = self.client_repo.get(client_id, agence_id=agence_id)
        if not client:
            raise ValueError("Client introuvable ou non autorisé")

        # 2. Vérification du bien (avec appartenance à l'agence)
        bien = self.bien_repo.get(bien_id, agence_id=agence_id)
        if not bien:
            raise ValueError("Bien introuvable ou non autorisé")

        # 3. Vérification de l'état du bien (doit être disponible)
        if bien.etat != EtatBien.DISPONIBLE:
            raise ValueError(
                f"Le bien n'est pas disponible pour la location. État actuel : {bien.etat.value}"
            )

        # 4. Vérification de la disponibilité (contrats actifs de l'agence)
        conflits = self.contrat_repo.find_by_bien_et_periode(bien_id, date_debut, date_fin, agence_id=agence_id)
        if conflits:
            raise ValueError("Le bien est déjà loué sur cette période.")

        # 5. Validation de la durée
        jours = (date_fin - date_debut).days
        if jours <= 0:
            raise ValueError("La durée de location doit être d'au moins un jour.")

        # 6. Récupération du prix unitaire depuis le Value Object PrixHT
        prix_base = bien.prix_unitaire_ht.amount  # Decimal

        # 7. Récupération de la catégorie du bien (si présente)
        categorie_id = getattr(bien, 'categorie_id', None)

        # 8. Calcul du prix final via le service de tarification
        prix_final = self.tarif_service.calculer_prix(
            agence_id=agence_id,
            prix_base=prix_base,
            duree=jours,
            bien_id=bien_id,
            categorie_id=categorie_id,
            date_debut=date_debut
        )

        # 9. Création du contrat (avec agence_id)
        contrat = Contrat(
            client_id=client_id,
            bien_id=bien_id,
            date_debut=date_debut,
            date_fin=date_fin,
            montant_total=Montant(prix_final),
            agence_id=agence_id
        )

        # 10. Persistance
        self.contrat_repo.add(contrat)

        return contrat