import pytest
from administration.domain.entities.agence import Agence
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email

def test_creer_agence():
    adresse = Adresse(
        rue="1 rue de Paris",
        code_postal="75001",
        ville="Paris",
        pays="France"
    )
    tel = Telephone("0123456789")
    email = Email("contact@agence.fr")
    # Le champ `code` est obligatoire dans l'entité Agence
    code = CodeAgence("AG001")
    agence = Agence(
        code=code,
        nom="Agence Test",
        adresse=adresse,
        telephone=tel,
        email=email
    )
    assert agence.nom == "Agence Test"