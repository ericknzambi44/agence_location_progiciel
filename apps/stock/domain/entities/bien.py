from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from shared_kernel.domain.value_objects.email import Email 

class EtatBien(Enum):
    DISPONIBLE = "disponible"
    EN_MAINTENANCE = "en_maintenance"
    ENDOMMAGE = "endommage"
    ARCHIVE = "archive"

class BienValidationError(Enum):
    REFERENCE_VIDE = "La référence du bien ne peut pas être vide."
    REFERENCE_TROP_LONGUE = "La référence ne peut pas dépasser 50 caractères."
    NOM_VIDE = "Le nom du bien est obligatoire."
    PRIX_UNITAIRE_NEGATIF = "Le prix unitaire doit être >= 0."
    DATE_ACHAT_FUTURE = "La date d'achat ne peut pas être dans le futur."
    ETAT_INVALIDE = "État du bien non reconnu."
    TRANSITION_ETAT_INVALIDE = "Transition d'état non autorisée."

@dataclass
class Bien:
    # Champs obligatoires (sans valeur par défaut)
    reference: str
    nom: str
    description: Optional[str] = None
    prix_unitaire_ht: float = 0.0
    date_achat: Optional[date] = None
    etat: EtatBien = EtatBien.DISPONIBLE
    # Champ avec défaut en dernier
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
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

    # Logique métier
    def passer_en_maintenance(self) -> None:
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.ENDOMMAGE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.EN_MAINTENANCE

    def liberer_apres_maintenance(self) -> None:
        if self.etat != EtatBien.EN_MAINTENANCE:
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.DISPONIBLE

    def signaler_endommagement(self) -> None:
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.EN_MAINTENANCE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.ENDOMMAGE

    def archiver(self) -> None:
        if self.etat == EtatBien.ARCHIVE:
            return
        self.etat = EtatBien.ARCHIVE