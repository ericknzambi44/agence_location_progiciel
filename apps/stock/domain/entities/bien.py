"""
Entité représentant un bien (article) à louer.
Contient la logique métier de base (changement d'état, validation).
La disponibilité pour la location est vérifiée par le module Location via les contrats.
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from stock.domain.value_objects.prix import PrixHT


class EtatBien(Enum):
    """États possibles d'un bien."""
    DISPONIBLE = "disponible"
    EN_MAINTENANCE = "en_maintenance"
    ENDOMMAGE = "endommage"
    ARCHIVE = "archive"


class BienValidationError(Enum):
    """Erreurs de validation de l'entité Bien."""
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
    Entité représentant un bien à louer.

    Attributes:
        reference (str): Référence unique du bien.
        nom (str): Nom du bien.
        description (Optional[str]): Description du bien.
        prix_unitaire_ht (PrixHT): Prix hors taxes par jour.
        date_achat (Optional[date]): Date d'achat du bien.
        etat (EtatBien): État actuel du bien.
        id (UUID): Identifiant unique (généré automatiquement).
    """
    reference: str
    nom: str
    prix_unitaire_ht: PrixHT          # Utilisation du Value Object
    description: Optional[str] = None
    date_achat: Optional[date] = None
    etat: EtatBien = EtatBien.DISPONIBLE
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Valide toutes les contraintes à l'instanciation."""
        self._validate_reference()
        self._validate_nom()
        self._validate_date_achat()
        self._validate_etat()

    def _validate_reference(self) -> None:
        """Vérifie que la référence est non vide et ne dépasse pas 50 caractères."""
        if not self.reference or not self.reference.strip():
            raise ValueError(BienValidationError.REFERENCE_VIDE.value)
        if len(self.reference) > 50:
            raise ValueError(BienValidationError.REFERENCE_TROP_LONGUE.value)

    def _validate_nom(self) -> None:
        """Vérifie que le nom est non vide."""
        if not self.nom or not self.nom.strip():
            raise ValueError(BienValidationError.NOM_VIDE.value)

    def _validate_date_achat(self) -> None:
        """Vérifie que la date d'achat n'est pas dans le futur."""
        if self.date_achat and self.date_achat > date.today():
            raise ValueError(BienValidationError.DATE_ACHAT_FUTURE.value)

    def _validate_etat(self) -> None:
        """Vérifie que l'état est une valeur valide de l'énumération."""
        if not isinstance(self.etat, EtatBien):
            raise ValueError(BienValidationError.ETAT_INVALIDE.value)

    # --- Méthodes de transition d'état (logique métier) ---

    def passer_en_maintenance(self) -> None:
        """
        Passe le bien en maintenance.
        Autorisé uniquement depuis les états DISPONIBLE ou ENDOMMAGE.
        """
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.ENDOMMAGE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.EN_MAINTENANCE

    def liberer_apres_maintenance(self) -> None:
        """
        Remet le bien disponible après maintenance.
        Autorisé uniquement depuis l'état EN_MAINTENANCE.
        """
        if self.etat != EtatBien.EN_MAINTENANCE:
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.DISPONIBLE

    def signaler_endommagement(self) -> None:
        """
        Signale un endommagement du bien.
        Autorisé depuis DISPONIBLE ou EN_MAINTENANCE.
        """
        if self.etat not in (EtatBien.DISPONIBLE, EtatBien.EN_MAINTENANCE):
            raise ValueError(BienValidationError.TRANSITION_ETAT_INVALIDE.value)
        self.etat = EtatBien.ENDOMMAGE

    def archiver(self) -> None:
        """
        Archive le bien (définitivement non louable).
        Autorisé depuis n'importe quel état (si déjà archivé, ne fait rien).
        """
        if self.etat == EtatBien.ARCHIVE:
            return
        self.etat = EtatBien.ARCHIVE