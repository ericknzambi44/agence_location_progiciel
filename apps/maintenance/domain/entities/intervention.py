from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List, Tuple
from decimal import Decimal
from maintenance.domain.entities.technicien import Technicien
from maintenance.domain.entities.piece_detachee import PieceDetachee
from enum import Enum

class StatutIntervention(Enum):
    PLANIFIEE = "planifiee"
    EN_COURS = "en_cours"
    TERMINEE = "terminee"
    ANNULEE = "annulee"

@dataclass
class Intervention:
    bien_id: UUID
    technicien: Technicien
    date_debut: datetime
    date_fin: datetime
    statut: StatutIntervention = StatutIntervention.PLANIFIEE
    pieces_utilisees: List[Tuple[PieceDetachee, int]] = field(default_factory=list)
    cout_main_oeuvre: Decimal = Decimal('0')
    cout_total: Decimal = Decimal('0')
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        # Utiliser timezone-aware pour la comparaison (UTC)
        now = datetime.now(timezone.utc)
        if self.date_debut < now:
            raise ValueError("La date de début ne peut pas être dans le passé")
        if self.date_fin <= self.date_debut:
            raise ValueError("La date de fin doit être postérieure à la date de début")

    def demarrer(self):
        if self.statut != StatutIntervention.PLANIFIEE:
            raise ValueError("Seule une intervention planifiée peut être démarrée")
        self.statut = StatutIntervention.EN_COURS

    def terminer(self):
        if self.statut != StatutIntervention.EN_COURS:
            raise ValueError("Seule une intervention en cours peut être terminée")
        self.statut = StatutIntervention.TERMINEE
        self.calculer_cout()

    def ajouter_piece(self, piece: PieceDetachee, quantite: int):
        if self.statut not in (StatutIntervention.PLANIFIEE, StatutIntervention.EN_COURS):
            raise ValueError("Impossible d'ajouter des pièces à une intervention terminée ou annulée")
        self.pieces_utilisees.append((piece, quantite))

    def calculer_cout(self):
        duree_heures = (self.date_fin - self.date_debut).total_seconds() / 3600
        self.cout_main_oeuvre = Decimal(str(duree_heures)) * self.technicien.cout_horaire
        cout_pieces = sum(p.prix_unitaire * q for p, q in self.pieces_utilisees)
        self.cout_total = self.cout_main_oeuvre + cout_pieces