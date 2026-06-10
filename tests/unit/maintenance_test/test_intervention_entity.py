import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from decimal import Decimal
from maintenance.domain.entities.intervention import Intervention
from maintenance.domain.entities.technicien import Technicien
from shared_kernel.domain.value_objects import PersonName, Email

def test_creer_intervention():
    technicien = Technicien(
        nom=PersonName("Dupont"),
        prenom=PersonName("Jean"),
        email=Email("jean@example.com"),
        cout_horaire=Decimal("25.0")
    )
    now = datetime.now()
    intervention = Intervention(
        bien_id=uuid4(),
        technicien=technicien,
        date_debut=now + timedelta(days=1),
        date_fin=now + timedelta(days=1, hours=2)
    )
    # Correction : statut est une chaîne, pas un enum
    assert intervention.statut == "planifiee"
    assert intervention.technicien == technicien
    assert intervention.date_debut is not None
    assert intervention.date_fin is not None

def test_demarrer_intervention():
    technicien = Technicien(
        nom=PersonName("Dupont"),
        prenom=PersonName("Jean"),
        email=Email("jean@example.com"),
        cout_horaire=Decimal("25.0")
    )
    now = datetime.now()
    intervention = Intervention(
        bien_id=uuid4(),
        technicien=technicien,
        date_debut=now + timedelta(days=1),
        date_fin=now + timedelta(days=1, hours=2)
    )
    intervention.demarrer()
    assert intervention.statut == "en_cours"

def test_ajouter_piece():
    # Créer une pièce factice (pour le test, on peut passer un objet simple)
    from maintenance.domain.entities.piece_detachee import PieceDetachee
    piece = PieceDetachee(
        reference="P001",
        nom="Clavier",
        prix_unitaire=Decimal("15.0"),
        stock=5
    )
    technicien = Technicien(
        nom=PersonName("Dupont"),
        prenom=PersonName("Jean"),
        email=Email("jean@example.com"),
        cout_horaire=Decimal("25.0")
    )
    now = datetime.now()
    intervention = Intervention(
        bien_id=uuid4(),
        technicien=technicien,
        date_debut=now + timedelta(days=1),
        date_fin=now + timedelta(days=1, hours=2)
    )
    intervention.demarrer()
    intervention.ajouter_piece(piece, 2)
    assert len(intervention.pieces_utilisees) == 1
    assert intervention.pieces_utilisees[0][0] == piece
    assert intervention.pieces_utilisees[0][1] == 2

def test_terminer_et_calculer_cout():
    from maintenance.domain.entities.piece_detachee import PieceDetachee
    piece = PieceDetachee(
        reference="P001",
        nom="Clavier",
        prix_unitaire=Decimal("15.0"),
        stock=5
    )
    technicien = Technicien(
        nom=PersonName("Dupont"),
        prenom=PersonName("Jean"),
        email=Email("jean@example.com"),
        cout_horaire=Decimal("25.0")
    )
    now = datetime.now()
    debut = now + timedelta(days=1)
    fin = now + timedelta(days=1, hours=2)  # 2 heures
    intervention = Intervention(
        bien_id=uuid4(),
        technicien=technicien,
        date_debut=debut,
        date_fin=fin
    )
    intervention.demarrer()
    intervention.ajouter_piece(piece, 2)
    cout_total = intervention.terminer()
    # Calcul attendu : (2h * 25) + (2 * 15) = 50 + 30 = 80
    assert cout_total == 80.0
    assert intervention.statut == "terminee"