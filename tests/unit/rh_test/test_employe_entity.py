import pytest
from datetime import date
from rh.domain.entities.employe import Employe
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from shared_kernel.domain.value_objects import PersonName, Email
from decimal import Decimal

def test_creer_employe():
    matricule = Matricule("EMP001")
    nom = PersonName("Dupont")
    prenom = PersonName("Jean")
    email = Email("jean@example.com")
    taux = TauxHoraire(Decimal("25.0"))
    employe = Employe(
        matricule=matricule,
        nom=nom,
        prenom=prenom,
        email=email,
        date_embauche=date(2025,1,1),
        taux_horaire=taux,
        poste="Technicien"
    )
    assert employe.matricule.value == "EMP001"