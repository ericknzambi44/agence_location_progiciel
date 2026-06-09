import pytest
from maintenance.domain.entities.piece_detachee import PieceDetachee
from decimal import Decimal

def test_creer_piece():
    piece = PieceDetachee(reference="P001", nom="Vis", prix_unitaire=Decimal("5.0"))
    assert piece.reference == "P001"
    assert piece.stock == 0