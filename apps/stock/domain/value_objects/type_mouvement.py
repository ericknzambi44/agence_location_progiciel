"""
Value Object : TypeMouvement.

Définit les différents types de mouvements de stock possibles.
"""

from enum import Enum


class TypeMouvement(Enum):
    """
    Types de mouvements de stock.
    """

    ENTREE = "entree"
    SORTIE = "sortie"
    RESERVATION = "reservation"
    ANNULATION_RESERVATION = "annulation_reservation"
    RETOUR = "retour"
    AJUSTEMENT = "ajustement"