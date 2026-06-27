"""
Value Object représentant une règle de tarification pour la maintenance.
Une règle peut être un forfait, une remise ou une majoration,
et s'applique sur le coût total d'une intervention (main-d'œuvre + pièces).

Attributs :
    - type: TypeRegleMaintenance (forfait, remise, majoration)
    - valeur: Decimal (montant ou pourcentage)
    - duree_min: int (durée minimale de l'intervention en heures)
    - duree_max: Optional[int] (durée maximale, None = illimité)
    - periode_debut: Optional[date] (début de la période d'application)
    - periode_fin: Optional[date] (fin de la période, None = indéfinie)
    - description: str (optionnel)
    - active: bool (True par défaut)
    - agence_id: UUID (pour associer la règle à une agence)
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum


class TypeRegleMaintenance(Enum):
    """Types de règles de tarification pour la maintenance."""
    FORFAIT = "forfait"
    REMISE = "remise"
    MAJORATION = "majoration"


@dataclass(frozen=True)
class RegleMaintenance:
    """
    Règle de tarification immuable pour la maintenance.
    Validation des contraintes à la construction.
    """
    type: TypeRegleMaintenance
    valeur: Decimal
    agence_id: UUID
    duree_min: int = 0
    duree_max: Optional[int] = None
    periode_debut: Optional[date] = None
    periode_fin: Optional[date] = None
    description: str = ""
    active: bool = True

    def __post_init__(self):
        """Valide les données de la règle."""
        if self.valeur < 0:
            raise ValueError("La valeur d'une règle ne peut pas être négative.")
        if self.type == TypeRegleMaintenance.FORFAIT and self.valeur <= 0:
            raise ValueError("Un forfait doit avoir une valeur strictement positive.")
        if self.duree_min < 0:
            raise ValueError("La durée minimale doit être >= 0.")
        if self.duree_max is not None and self.duree_max < self.duree_min:
            raise ValueError("La durée maximale doit être >= la durée minimale.")
        if self.periode_debut and self.periode_fin and self.periode_debut > self.periode_fin:
            raise ValueError("La période de début doit être avant la période de fin.")

    def est_applicable(self, duree: float, date_intervention: date) -> bool:
        """
        Vérifie si la règle s'applique à une intervention donnée.

        Args:
            duree: durée de l'intervention en heures
            date_intervention: date de l'intervention

        Returns:
            True si la règle s'applique, False sinon.
        """
        if not self.active:
            return False
        # Vérification de la durée
        if duree < self.duree_min:
            return False
        if self.duree_max is not None and duree > self.duree_max:
            return False
        # Vérification de la période
        if self.periode_debut and date_intervention < self.periode_debut:
            return False
        if self.periode_fin and date_intervention > self.periode_fin:
            return False
        return True

    def appliquer(self, cout_total: Decimal) -> Decimal:
        """
        Applique la règle sur le coût total de l'intervention.

        Pour un forfait, remplace complètement le coût.
        Pour une remise, réduit le coût d'un pourcentage.
        Pour une majoration, augmente le coût d'un pourcentage.
        """
        if self.type == TypeRegleMaintenance.FORFAIT:
            return self.valeur
        elif self.type == TypeRegleMaintenance.REMISE:
            return cout_total * (Decimal(1) - self.valeur / Decimal(100))
        elif self.type == TypeRegleMaintenance.MAJORATION:
            return cout_total * (Decimal(1) + self.valeur / Decimal(100))
        return cout_total