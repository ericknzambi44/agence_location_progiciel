"""
Value Object représentant une règle de tarification.
Une règle peut être un forfait, une remise ou une majoration,
et peut s'appliquer à un bien spécifique, à une catégorie de biens,
ou à tous les biens (global).

Attributs :
    - type: TypeRegle (forfait, remise, majoration)
    - valeur: Decimal (montant ou pourcentage)
    - duree_min: int (jours minimum pour que la règle s'applique)
    - duree_max: Optional[int] (jours maximum, None = illimité)
    - bien_id: Optional[UUID] (si renseigné, s'applique uniquement à ce bien)
    - categorie_id: Optional[UUID] (si renseigné, s'applique à tous les biens de cette catégorie)
    - periode_debut: Optional[date] (début de la période d'application)
    - periode_fin: Optional[date] (fin de la période, None = indéfinie)
    - description: str (optionnel)
    - active: bool (True par défaut)

Règles de priorité :
    1. Une règle avec bien_id est prioritaire sur une règle avec categorie_id.
    2. Si bien_id et categorie_id sont None, la règle est globale.
    3. Les forfaits sont appliqués en premier et remplacent tout autre calcul.
    4. Les remises et majorations s'appliquent successivement sur le prix total.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum


class TypeRegle(Enum):
    """Types de règles de tarification."""
    FORFAIT = "forfait"
    REMISE = "remise"
    MAJORATION = "majoration"


@dataclass(frozen=True)
class RegleTarification:
    """
    Règle de tarification immuable.
    Validation des contraintes à la construction.
    """
    type: TypeRegle
    valeur: Decimal
    duree_min: int
    duree_max: Optional[int] = None
    bien_id: Optional[UUID] = None
    categorie_id: Optional[UUID] = None
    periode_debut: Optional[date] = None
    periode_fin: Optional[date] = None
    description: str = ""
    active: bool = True

    def __post_init__(self):
        """Valide les données de la règle."""
        if self.valeur < 0:
            raise ValueError("La valeur d'une règle ne peut pas être négative.")
        if self.type == TypeRegle.FORFAIT and self.valeur <= 0:
            raise ValueError("Un forfait doit avoir une valeur strictement positive.")
        if self.duree_min < 0:
            raise ValueError("La durée minimale doit être >= 0.")
        if self.duree_max is not None and self.duree_max < self.duree_min:
            raise ValueError("La durée maximale doit être >= la durée minimale.")
        if self.periode_debut and self.periode_fin and self.periode_debut > self.periode_fin:
            raise ValueError("La période de début doit être avant la période de fin.")
        if self.bien_id and self.categorie_id:
            raise ValueError("Une règle ne peut pas cibler à la fois un bien et une catégorie.")

    def est_applicable(self, bien_id: UUID, categorie_id: Optional[UUID],
                       duree: int, date_debut: date) -> bool:
        """
        Vérifie si la règle s'applique à une location donnée.

        Args:
            bien_id: ID du bien loué
            categorie_id: ID de la catégorie du bien (ou None)
            duree: nombre de jours de la location
            date_debut: date de début de la location

        Returns:
            True si la règle s'applique, False sinon.
        """
        if not self.active:
            return False
        # Vérification des durées
        if duree < self.duree_min:
            return False
        if self.duree_max is not None and duree > self.duree_max:
            return False
        # Vérification du bien / catégorie
        if self.bien_id is not None and self.bien_id != bien_id:
            return False
        if self.categorie_id is not None:
            if categorie_id is None or self.categorie_id != categorie_id:
                return False
        # Vérification de la période
        if self.periode_debut and date_debut < self.periode_debut:
            return False
        if self.periode_fin and date_debut > self.periode_fin:
            return False
        return True

    def appliquer(self, prix_total: Decimal) -> Decimal:
        """
        Applique la règle sur un prix total (déjà multiplié par la durée).
        Pour un forfait, remplace complètement le prix.
        Pour une remise, réduit le prix d'un pourcentage.
        Pour une majoration, augmente le prix d'un pourcentage.
        """
        if self.type == TypeRegle.FORFAIT:
            return self.valeur
        elif self.type == TypeRegle.REMISE:
            return prix_total * (Decimal(1) - self.valeur / Decimal(100))
        elif self.type == TypeRegle.MAJORATION:
            return prix_total * (Decimal(1) + self.valeur / Decimal(100))
        return prix_total