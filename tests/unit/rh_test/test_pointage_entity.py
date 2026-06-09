import pytest
from datetime import datetime
from uuid import uuid4
from rh.domain.entities.pointage import Pointage

def test_creer_pointage():
    pointage = Pointage(employe_id=uuid4(), type="ENTRY")
    assert pointage.type == "ENTRY"
    assert pointage.horodatage is not None