"""
Entité centrale du module Stock : Bien (article à louer).
Contient toute la logique métier et validation.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4



class EtatBien(Enum):
    DISPONIBLE = "disponible"
    EN_MAINTENANCE = "en_maintenance"
    ENDOMMAGE = "endommage"
    ARCHIVE = "archive"


class BienValidationError(Enum):
    """Erreurs métier pour l'entité Bien."""
    REFERENCE_VIDE = "La référence du bien ne peut pas être vide."
    REFERENCE_TROP_LONGUE = "La référence ne peut pas dépasser 50 caractères."
    NOM_VIDE = "Le nom du bien est obligatoire."
    PRIX_UNITAIRE_NEGATIF = "Le prix unitaire doit être >= 0."
    DATE_ACHAT_FUTURE = "La date d'achat ne peut pas être dans le futur."
    ETAT_INVALIDE = "État du bien non reconnu."
    TRANSITION_ETAT_INVALIDE = "Transition d'état non autorisée."


@dataclass
class Bien:
    """
    Entité représentant un bien physique ou numérique à louer.
    L'identifiant est généré automatiquement (UUID).
    """
    id: UUID = field(default_factory=uuid4)
    reference: str
    nom: str
    description: Optional[str] = None
    prix_unitaire_ht: float = 0.0
    date_achat: Optional[date] = None
    etat: EtatBien = EtatBien.DISPONIBLE

    def __post_init__(self) -> None:
        """Validation métier obligatoire à la construction."""
        self._validate_reference()
        self._validate_nom()
        self._validate_prix()
        self._validate_date_achat()
        self._validate_etat()

    def _validate_reference(self) -> None:
        if not self.reference or not self.reference.strip():
            raise ValueError(BienValidationError.REFERENCE_VIDE.value)
        if len(self.reference) > 50:
            raise ValueError(BienValidationError.REFERENCE_TROP_LONGUE.value)

    def _validate_nom(self) -> None:
        if not self.nom or not self.nom.strip():
            raise ValueError(BienValidationError.NOM_VIDE.value)

    def _validate_prix(self) -> None:
        if self.prix_unitaire_ht < 0:
            raise ValueError(BienValidationError.PRIX_UNITAIRE_NEGATIF.value)

    def _validate_date_achat(self) -> None:
        if self.date_achat and self.date_achat > date.today():
            raise ValueError(BienValidationError.DATE_ACHAT_FUTURE.value)

    def _validate_etat(self) -> None:
        if not isinstance(self.etat, EtatBien):
            raise ValueError(BienValidationError.ETAT_INVALIDE.value)

    # --- Logique métier ---
    def passer_en_maintenance(self) -> None:
        """Transition vers l'état 'en maintenance'."""
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.ENDOMMAGE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.EN_MAINTENANCE

    def liberer_apres_maintenance(self) -> None:
        """Remet disponible après maintenance."""
        if self.etat != EtatBien.EN_MAINTENANCE:
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.DISPONIBLE

    def signaler_endommagement(self) -> None:
        """Passe à l'état endommagé (depuis disponible ou maintenance)."""
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.EN_MAINTENANCE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.ENDOMMAGE

    def archiver(self) -> None:
        """Archive le bien (définitivement non louable)."""
        if self.etat == EtatBien.ARCHIVE:
            return
        if self.etat == EtatBien.EN_MAINTENANCE:
            # On peut autoriser l'archivage même en maintenance
            self.etat = EtatBien.ARCHIVE
        else:
            self.etat = EtatBien.ARCHIVE
    