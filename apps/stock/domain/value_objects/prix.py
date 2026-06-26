"""
Value Object représentant un prix hors taxes (HT).
Valide le montant (positif, inférieur à 1e12) et la devise (ISO 4217).
Immuable et utilisable comme type dans les entités du domaine.
"""
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class PrixValidationError(Enum):
    """Énumération des erreurs de validation du prix."""
    NEGATIF = "Le prix ne peut pas être négatif."
    TROP_GRAND = "Le prix dépasse la limite autorisée (1e12)."
    DEVISE_INVALIDE = "La devise n'est pas reconnue."


@dataclass(frozen=True)
class PrixHT:
    """
    Prix hors taxes avec devise.
    Attributes:
        amount (Decimal): Montant du prix.
        currency (str): Code devise ISO 4217 (défaut: USD).
    """
    amount: Decimal
    currency: str = "USD"

    # Devises autorisées selon la norme ISO 4217 (principales)
    _ALLOWED_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "INR", "BRL"}

    def __post_init__(self):
        """Valide le montant et la devise à la construction."""
        if self.amount < 0:
            raise ValueError(PrixValidationError.NEGATIF.value)
        if self.amount > Decimal('1e12'):
            raise ValueError(PrixValidationError.TROP_GRAND.value)
        self._validate_currency()

    def _validate_currency(self) -> None:
        """Vérifie que la devise est dans la liste autorisée."""
        if self.currency not in self._ALLOWED_CURRENCIES:
            raise ValueError(PrixValidationError.DEVISE_INVALIDE.value)