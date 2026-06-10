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
    bien_id: UUID
    id: Optional[UUID] = None
    technicien: Optional[Technicien] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    statut: str = "planifiee"
    pieces_utilisees: List[Tuple[PieceDetachee, int]] = field(default_factory=list)
    _cout_main_oeuvre: Decimal = field(default=Decimal(0), repr=False)
    _cout_total: Decimal = field(default=Decimal(0), repr=False)

    def __post_init__(self):
        if self.date_debut and self.date_fin and self.date_debut >= self.date_fin:
            raise ValueError("La date de début doit être antérieure à la date de fin")
        if self.statut not in ("planifiee", "en_cours", "terminee", "annulee"):
            raise ValueError("Statut invalide")

    def planifier(self, technicien: Technicien, debut: datetime, fin: datetime) -> None:
        self.technicien = technicien
        self.date_debut = debut
        self.date_fin = fin
        self.statut = "planifiee"

    def demarrer(self) -> None:
        if self.statut != "planifiee":
            raise ValueError("Seule une intervention planifiée peut démarrer")
        self.statut = "en_cours"

    def ajouter_piece(self, piece: PieceDetachee, quantite: int) -> None:
        if self.statut not in ("planifiee", "en_cours"):
            raise ValueError("Impossible d'ajouter des pièces")
        self.pieces_utilisees.append((piece, quantite))

    def terminer(self) -> float:
        if self.statut != "en_cours":
            raise ValueError("Seule une intervention en cours peut être terminée")
        if not self.date_debut or not self.date_fin:
            raise ValueError("Dates non définies")
        self.statut = "terminee"
        return self.calculer_cout()

    def calculer_cout(self) -> float:
        if self.statut not in ("en_cours", "terminee"):
            raise ValueError("Coût calculable seulement pour intervention en cours/terminée")
        if not self.date_debut or not self.date_fin:
            raise ValueError("Dates manquantes")
        duree_heures = (self.date_fin - self.date_debut).total_seconds() / 3600
        if duree_heures <= 0:
            raise ValueError("Durée invalide")
        if not self.technicien or self.technicien.cout_horaire <= 0:
            raise ValueError("Coût horaire technicien invalide")
        cout_main_oeuvre = Decimal(duree_heures) * Decimal(str(self.technicien.cout_horaire))
        cout_pieces = sum(Decimal(str(piece.prix_unitaire)) * quantite for piece, quantite in self.pieces_utilisees)
        cout_total = cout_main_oeuvre + cout_pieces
        self._cout_main_oeuvre = cout_main_oeuvre
        self._cout_total = cout_total
        return float(cout_total)