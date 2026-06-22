"""
Entité regroupant les règles de tarification pour une agence.
"""
from dataclasses import dataclass, field
from typing import List
from uuid import UUID
from decimal import Decimal
from datetime import date
from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle


@dataclass
class ReglesTarification:
    agence_id: UUID
    regles: List[RegleTarification] = field(default_factory=list)

    def ajouter(self, regle: RegleTarification) -> None:
        self.regles.append(regle)

    def supprimer(self, index: int) -> None:
        if 0 <= index < len(self.regles):
            del self.regles[index]

    def calculer_prix(self, prix_base: Decimal, duree: int, type_bien_id: UUID, date_debut: date) -> Decimal:
        """
        Calcule le prix total d'une location en fonction des règles.
        - Les forfaits sont des montants fixes (déjà totaux) et remplacent tout calcul.
        - Les remises/majorations s'appliquent sur le prix de base multiplié par la durée.
        """
        # 1. Calcul du prix total de base (prix unitaire * nombre de jours)
        prix_total_base = prix_base * Decimal(duree)

        # 2. Vérifier si un forfait s'applique (remplace le prix total)
        for regle in sorted(self.regles, key=lambda r: r.duree_min, reverse=True):
            if regle.type == TypeRegle.FORFAIT and regle.est_applicable(duree, type_bien_id, date_debut):
                return regle.valeur

        # 3. Application des remises / majorations sur le prix total
        prix = prix_total_base
        for regle in self.regles:
            if regle.type == TypeRegle.REMISE and regle.est_applicable(duree, type_bien_id, date_debut):
                prix *= (Decimal(1) - regle.valeur / Decimal(100))
            elif regle.type == TypeRegle.MAJORATION and regle.est_applicable(duree, type_bien_id, date_debut):
                prix *= (Decimal(1) + regle.valeur / Decimal(100))

        return prix