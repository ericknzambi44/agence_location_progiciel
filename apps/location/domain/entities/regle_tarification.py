"""
Entité regroupant les règles de tarification pour une agence.
Contient la logique d'application des règles sur un prix de base.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import date
from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle


@dataclass
class ReglesTarification:
    """
    Agrégat regroupant les règles de tarification d'une agence.
    """
    agence_id: UUID
    regles: List[RegleTarification] = field(default_factory=list)

    def ajouter(self, regle: RegleTarification) -> None:
        """Ajoute une règle à la liste."""
        self.regles.append(regle)

    def supprimer(self, index: int) -> None:
        """Supprime une règle par son index."""
        if 0 <= index < len(self.regles):
            del self.regles[index]

    def calculer_prix(self, prix_base: Decimal, duree: int,
                      bien_id: UUID, categorie_id: Optional[UUID],
                      date_debut: date) -> Decimal:
        """
        Calcule le prix total d'une location en appliquant les règles.

        Étapes :
            1. Calcul du prix total de base (prix unitaire × nombre de jours).
            2. Recherche d'un forfait applicable (le plus restrictif en durée min).
               Si trouvé, il remplace le prix total.
            3. Sinon, application successive des remises et majorations
               applicables sur le prix total de base.

        Args:
            prix_base: prix unitaire du bien (par jour)
            duree: nombre de jours de location
            bien_id: ID du bien loué
            categorie_id: ID de la catégorie du bien (ou None)
            date_debut: date de début de la location

        Returns:
            Decimal: prix total après application des règles.
        """
        # 1. Prix total de base
        prix_total_base = prix_base * Decimal(duree)

        # 2. Application des forfaits (prioritaires)
        # On trie les forfaits par duree_min décroissante pour prendre le plus spécifique
        forfaits = [r for r in self.regles if r.type == TypeRegle.FORFAIT]
        for regle in sorted(forfaits, key=lambda r: r.duree_min, reverse=True):
            if regle.est_applicable(bien_id, categorie_id, duree, date_debut):
                return regle.appliquer(prix_total_base)  # remplace total

        # 3. Application des remises et majorations
        prix = prix_total_base
        for regle in self.regles:
            if regle.type in (TypeRegle.REMISE, TypeRegle.MAJORATION):
                if regle.est_applicable(bien_id, categorie_id, duree, date_debut):
                    prix = regle.appliquer(prix)  # applique la règle sur le prix courant

        return prix