"""
Entité domaine représentant une intervention de maintenance.
Contient toute la logique métier : planification, démarrage, ajout de pièces,
terminaison, calcul des coûts, et vérification des conflits de planning.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Tuple, Optional
from uuid import UUID

from maintenance.domain.value_objects.cout import Cout
from maintenance.domain.entities.technicien import Technicien
from maintenance.domain.entities.piece_detachee import PieceDetachee


@dataclass
class Intervention:
    """
    Intervention technique sur un bien.
    Gère son cycle de vie et ses coûts.
    """

    bien_id: UUID
    id: Optional[UUID] = None
    technicien: Optional[Technicien] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    statut: str = "planifiee"  # planifiee | en_cours | terminee | annulee

    # Liste des pièces utilisées, avec leur quantité
    pieces_utilisees: List[Tuple[PieceDetachee, int]] = field(default_factory=list)

    # Coûts internes (non exposés directement)
    _cout_main_oeuvre: Decimal = field(default=Decimal(0), repr=False)
    _cout_total: Decimal = field(default=Decimal(0), repr=False)

    def __post_init__(self):
        """Validation des contraintes à l'instanciation."""
        if self.date_debut and self.date_fin and self.date_debut >= self.date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin")
        if self.statut not in ("planifiee", "en_cours", "terminee", "annulee"):
            raise ValueError("Statut invalide")

    def planifier(self, technicien: Technicien, debut: datetime, fin: datetime) -> None:
        """
        Affecte un technicien et définit la plage horaire de l'intervention.
        Passe le statut à 'planifiee'.
        """
        self.technicien = technicien
        self.date_debut = debut
        self.date_fin = fin
        self.statut = "planifiee"

    def demarrer(self) -> None:
        """Passe l'intervention en cours d'exécution."""
        if self.statut != "planifiee":
            raise ValueError("Seule une intervention planifiée peut démarrer")
        self.statut = "en_cours"

    def ajouter_piece(self, piece: PieceDetachee, quantite: int) -> None:
        """
        Ajoute ou met à jour une pièce détachée dans l'intervention.
        Si la pièce est déjà présente, sa quantité est augmentée.
        """
        if self.statut not in ("planifiee", "en_cours"):
            raise ValueError("Impossible d'ajouter des pièces à une intervention terminée ou annulée")

        # Recherche d'une occurrence existante de la même pièce
        for i, (p, q) in enumerate(self.pieces_utilisees):
            if p.id == piece.id:
                # Mise à jour de la quantité
                self.pieces_utilisees[i] = (p, q + quantite)
                return

        # Nouvelle entrée
        self.pieces_utilisees.append((piece, quantite))

    def terminer(self) -> float:
        """
        Termine l'intervention, calcule le coût et retourne le total.
        """
        if self.statut != "en_cours":
            raise ValueError("Seule une intervention en cours peut être terminée")
        if not self.date_debut or not self.date_fin:
            raise ValueError("Dates non définies")
        self.statut = "terminee"
        return self.calculer_cout()

    def calculer_cout(self) -> float:
        """
        Calcule le coût total de l'intervention :
        - main-d'œuvre = durée (heures) × taux horaire du technicien
        - pièces = somme (prix unitaire × quantité)
        Met à jour les attributs internes _cout_main_oeuvre et _cout_total.
        """
        if self.statut not in ("en_cours", "terminee"):
            raise ValueError("Coût calculable seulement pour intervention en cours ou terminée")
        if not self.date_debut or not self.date_fin:
            raise ValueError("Dates manquantes")

        duree_heures = (self.date_fin - self.date_debut).total_seconds() / 3600
        if duree_heures <= 0:
            raise ValueError("Durée invalide")

        if not self.technicien or self.technicien.cout_horaire <= 0:
            raise ValueError("Coût horaire technicien invalide")

        # Calcul de la main-d'œuvre
        cout_main_oeuvre = Decimal(duree_heures) * Decimal(str(self.technicien.cout_horaire))

        # Calcul du coût des pièces
        cout_pieces = sum(
            Decimal(str(piece.prix_unitaire)) * quantite
            for piece, quantite in self.pieces_utilisees
        )

        # Total
        cout_total = cout_main_oeuvre + cout_pieces

        # Mémorisation des coûts (non persistés directement, mais utiles pour l'affichage)
        self._cout_main_oeuvre = cout_main_oeuvre
        self._cout_total = cout_total

        return float(cout_total)

    def est_en_conflit_avec(self, autre: 'Intervention') -> bool:
        """
        Vérifie si cette intervention chevauche une autre intervention
        (même technicien ou même bien) sur la même plage horaire.

        Args:
            autre (Intervention): l'autre intervention à comparer

        Returns:
            bool: True si conflit, False sinon
        """
        if not self.date_debut or not self.date_fin or not autre.date_debut or not autre.date_fin:
            return False  # Pas de conflit si les dates ne sont pas définies

        # Chevauchement des plages horaires
        chevauchement = self.date_debut < autre.date_fin and autre.date_debut < self.date_fin
        if not chevauchement:
            return False

        # Conflit si même technicien ou même bien
        if self.technicien and autre.technicien and self.technicien.id == autre.technicien.id:
            return True
        if self.bien_id == autre.bien_id:
            return True

        return False

    @property
    def cout_total(self) -> Decimal:
        """Retourne le coût total calculé (lecture seule)."""
        return self._cout_total