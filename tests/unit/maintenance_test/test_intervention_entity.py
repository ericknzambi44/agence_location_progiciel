import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from maintenance.domain.entities.intervention import Intervention, StatutIntervention
from maintenance.domain.entities.technicien import Technicien
from shared_kernel.domain.value_objects import PersonName, Email
from decimal import Decimal

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
    assert intervention.statut == StatutIntervention.PLANIFIEE