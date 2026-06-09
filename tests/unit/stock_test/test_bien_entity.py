import pytest
from datetime import date
from stock.domain.entities.bien import Bien, EtatBien

def test_creer_bien_valide():
    bien = Bien(
        reference="REF123",
        nom="Test",
        prix_unitaire_ht=100.0,
        date_achat=date(2023, 1, 1)
    )
    assert bien.reference == "REF123"
    assert bien.etat == EtatBien.DISPONIBLE

def test_reference_invalide():
    with pytest.raises(ValueError, match="La référence du bien ne peut pas être vide"):
        Bien(reference="", nom="Test")

def test_prix_negatif():
    with pytest.raises(ValueError, match="Le prix unitaire doit être >= 0"):
        Bien(reference="REF", nom="Test", prix_unitaire_ht=-10)

def test_transition_etat():
    bien = Bien(reference="R1", nom="Test")
    assert bien.etat == EtatBien.DISPONIBLE

    # disponible -> en maintenance
    bien.passer_en_maintenance()
    assert bien.etat == EtatBien.EN_MAINTENANCE

    # en maintenance -> disponible
    bien.liberer_apres_maintenance()
    assert bien.etat == EtatBien.DISPONIBLE

    # Transition invalide : libérer alors que l'état est disponible
    with pytest.raises(ValueError, match="Transition d'état non autorisée"):
        bien.liberer_apres_maintenance()

    # Test endommagement depuis disponible (correction du nom de méthode)
    bien.signaler_endommagement()   # ✅ pas 'signalier'
    assert bien.etat == EtatBien.ENDOMMAGE

    # endommagé -> en maintenance (autorisé)
    bien.passer_en_maintenance()
    assert bien.etat == EtatBien.EN_MAINTENANCE

    # en maintenance -> disponible
    bien.liberer_apres_maintenance()
    assert bien.etat == EtatBien.DISPONIBLE