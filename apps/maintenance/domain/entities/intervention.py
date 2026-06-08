from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from stock.domain.entities.bien import Bien  # dépendance externe mais domaine, OK car stock est un module voisin
from maintenance.domain.entities.technicien import Technicien
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.domain.value_objects.duree import Duree
from maintenance.domain.value_objects.cout import Cout
from maintenance.domain.enums.error_codes import InterventionError, CalculCoutError

class StatutIntervention(Enum):
    PLANIFIEE = "planifiee"
    EN_COURS = "en_cours"
    TERMINEE = "terminee"
    ANNULEE = "annulee"

@dataclass
class Intervention:
    id: UUID = field(default_factory=uuid4)
    bien: Bien
    technicien: Optional[Technicien] = None
    date_debut_prevue: Optional[datetime] = None
    date_fin_prevue: Optional[datetime] = None
    date_debut_reelle: Optional[datetime] = None
    date_fin_reelle: Optional[datetime] = None
    statut: StatutIntervention = StatutIntervention.PLANIFIEE
    pieces_utilisees: List[PieceDetachee] = field(default_factory=list)
    description_panne: str = ""
    rapport_final: str = ""
    cout_total: Optional[Cout] = None

    def __post_init__(self):
        self._validate_dates()
        if self.statut not in StatutIntervention:
            raise ValueError(InterventionError.INTERVENTION_SANS_TECHNICIEN.value)  # temporaire

    def _validate_dates(self):
        if self.date_debut_prevue and self.date_fin_prevue:
            if self.date_debut_prevue >= self.date_fin_prevue:
                raise ValueError(InterventionError.DATE_FIN_AVANT_DATE_DEBUT.value)
        if self.date_debut_reelle and self.date_fin_reelle:
            if self.date_debut_reelle >= self.date_fin_reelle:
                raise ValueError("Les dates réelles sont incohérentes.")

    # --- Logique métier ---
    def planifier(self, debut: datetime, fin: datetime, technicien: Technicien):
        if self.statut != StatutIntervention.PLANIFIEE:
            raise ValueError(InterventionError.INTERVENTION_DEJA_CLOTUREE.value)
        if debut < datetime.now():
            raise ValueError(InterventionError.DATE_DEBUT_INFERIEURE_A_AUJOURD_HUI.value)
        if debut >= fin:
            raise ValueError(InterventionError.DATE_FIN_AVANT_DATE_DEBUT.value)
        self.date_debut_prevue = debut
        self.date_fin_prevue = fin
        self.technicien = technicien
        # Ici on pourrait émettre un événement de domaine

    def demarrer(self):
        if self.statut != StatutIntervention.PLANIFIEE:
            raise ValueError("Seule une intervention planifiée peut démarrer.")
        if not self.technicien:
            raise ValueError(InterventionError.INTERVENTION_SANS_TECHNICIEN.value)
        self.statut = StatutIntervention.EN_COURS
        self.date_debut_reelle = datetime.now()

    def ajouter_piece(self, piece: PieceDetachee):
        if self.statut in (StatutIntervention.TERMINEE, StatutIntervention.ANNULEE):
            raise ValueError(InterventionError.INTERVENTION_DEJA_CLOTUREE.value)
        self.pieces_utilisees.append(piece)

    def terminer(self, rapport: str):
        if self.statut != StatutIntervention.EN_COURS:
            raise ValueError("Seule une intervention en cours peut être terminée.")
        self.statut = StatutIntervention.TERMINEE
        self.date_fin_reelle = datetime.now()
        self.rapport_final = rapport
        self.calculer_cout()

    def calculer_cout(self) -> Cout:
        if not self.date_debut_reelle or not self.date_fin_reelle:
            raise ValueError(CalculCoutError.DUREE_NON_DEFINIE.value)
        duree = Duree((self.date_fin_reelle - self.date_debut_reelle).total_seconds() / 3600.0)
        if not self.technicien:
            raise ValueError(CalculCoutError.TARIF_TECHNICIEN_NON_RENSEIGNE.value)
        cout_main_oeuvre = Cout(Decimal(str(self.technicien.cout_horaire * duree.heures)))
        cout_pieces = Cout(sum((p.prix_unitaire.montant * p.quantite_utilisee for p in self.pieces_utilisees), Decimal(0)))
        cout_total = cout_main_oeuvre + cout_pieces
        self.cout_total = cout_total
        return cout_total