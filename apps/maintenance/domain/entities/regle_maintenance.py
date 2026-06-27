"""
Entité regroupant les règles de tarification pour la maintenance.
Contient la logique d'application des règles sur le coût d'une intervention.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import date
from maintenance.domain.value_objects.regle_maintenance import (
    RegleMaintenance, TypeRegleMaintenance
)
from maintenance.domain.value_objects.duree import Duree
from maintenance.domain.value_objects.cout import Cout


@dataclass
class ReglesMaintenance:
    """
    Agrégat regroupant les règles de tarification pour une agence.
    """
    agence_id: UUID
    regles: List[RegleMaintenance] = field(default_factory=list)

    def ajouter(self, regle: RegleMaintenance) -> None:
        """Ajoute une règle à la liste."""
        self.regles.append(regle)

    def supprimer(self, index: int) -> None:
        """Supprime une règle par son index."""
        if 0 <= index < len(self.regles):
            del self.regles[index]

    def calculer_cout(self, cout_base: Cout, duree: Duree, date_intervention: date) -> Cout:
        """
        Applique les règles de tarification sur le coût de base d'une intervention.

        Étapes :
            1. Recherche d'un forfait applicable (le plus restrictif en durée min).
               Si trouvé, il remplace le coût total.
            2. Sinon, application successive des remises et majorations
               applicables sur le coût de base.

        Args:
            cout_base: coût de base (main-d'œuvre + pièces) avant règles
            duree: durée de l'intervention
            date_intervention: date de l'intervention

        Returns:
            Cout: coût final après application des règles.
        """
        # 1. Application des forfaits (prioritaires)
        # On trie les forfaits par duree_min décroissante pour prendre le plus spécifique
        forfaits = [r for r in self.regles if r.type == TypeRegleMaintenance.FORFAIT]
        for regle in sorted(forfaits, key=lambda r: r.duree_min, reverse=True):
            if regle.est_applicable(duree.heures, date_intervention):
                return Cout(regle.appliquer(cout_base.valeur))

        # 2. Application des remises et majorations
        prix = cout_base.valeur
        for regle in self.regles:
            if regle.type in (TypeRegleMaintenance.REMISE, TypeRegleMaintenance.MAJORATION):
                if regle.est_applicable(duree.heures, date_intervention):
                    prix = regle.appliquer(prix)

        return Cout(prix)