"""
Service de tarification dynamique.
Centralise la logique d'application des règles de tarification.
"""
from uuid import UUID
from decimal import Decimal
from datetime import date
from location.domain.repositories.regle_tarification_repository import RegleTarificationRepository
from location.domain.entities.regle_tarification import ReglesTarification


class TarificationService:
    """
    Service métier pour la gestion et l'application des règles de tarification.
    """

    def __init__(self, repo: RegleTarificationRepository):
        self.repo = repo

    def get_regles(self, agence_id: UUID) -> ReglesTarification:
        """
        Récupère les règles de tarification pour une agence donnée.
        Retourne un agrégat vide si aucune règle n'est définie.
        """
        regles = self.repo.get(agence_id)
        if regles is None:
            regles = ReglesTarification(agence_id=agence_id, regles=[])
        return regles

    def sauvegarder_regles(self, regles: ReglesTarification) -> None:
        """
        Sauvegarde (remplace) l'ensemble des règles pour une agence.
        """
        self.repo.save(regles)

    def calculer_prix(self, agence_id: UUID, prix_base: Decimal, duree: int,
                      bien_id: UUID, categorie_id: UUID | None, date_debut: date) -> Decimal:
        """
        Calcule le prix final d'une location en appliquant les règles de tarification.

        Args:
            agence_id: ID de l'agence (pour récupérer ses règles)
            prix_base: prix unitaire du bien (par jour)
            duree: nombre de jours de la location
            bien_id: ID du bien loué
            categorie_id: ID de la catégorie du bien (ou None)
            date_debut: date de début de la location

        Returns:
            Decimal: prix total après application des règles (ou prix de base × durée si aucune règle)
        """
        # Récupération des règles de l'agence
        regles = self.repo.get(agence_id)
        if regles is None:
            # Aucune règle définie : retour du prix total de base
            return prix_base * Decimal(duree)

        # Délégation du calcul à l'agrégat
        return regles.calculer_prix(
            prix_base=prix_base,
            duree=duree,
            bien_id=bien_id,
            categorie_id=categorie_id,
            date_debut=date_debut
        )