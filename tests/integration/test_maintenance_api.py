import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from maintenance.infrastructure.models import TechnicienModel, PieceDetacheeModel

pytestmark = pytest.mark.django_db

class TestMaintenanceAPI:
    def test_planifier_intervention(self, authenticated_client):
        # Créer un bien via l'API Stock
        stock_url = reverse('bien-list')
        bien_resp = authenticated_client.post(stock_url, {
            "reference": "B001", "nom": "Ordinateur",
            "prix_unitaire_ht": 1200.00, "etat": "disponible"
        }, format='json')
        assert bien_resp.status_code == 201
        bien_id = bien_resp.data['id']

        technicien = TechnicienModel.objects.create(
            nom="Dupont", prenom="Jean", email="jean@example.com", cout_horaire=25.0
        )
        now = timezone.now()
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (now + timedelta(days=1)).isoformat(),
            "date_fin": (now + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        url = reverse('intervention-list')
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['statut'] == 'planifiee'

    def test_ajouter_piece_et_terminer(self, authenticated_client):
        # Créer un bien
        stock_url = reverse('bien-list')
        bien_resp = authenticated_client.post(stock_url, {
            "reference": "B002", "nom": "Ordinateur",
            "prix_unitaire_ht": 1200.00, "etat": "disponible"
        }, format='json')
        assert bien_resp.status_code == 201
        bien_id = bien_resp.data['id']

        technicien = TechnicienModel.objects.create(
            nom="Martin", prenom="Pierre", email="pierre@example.com", cout_horaire=30.0
        )
        piece = PieceDetacheeModel.objects.create(
            reference="P002", nom="Clavier", prix_unitaire=15.0, stock=5
        )
        now = timezone.now()
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (now + timedelta(days=1)).isoformat(),
            "date_fin": (now + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        url = reverse('intervention-list')
        create_resp = authenticated_client.post(url, data, format='json')
        assert create_resp.status_code == 201
        intervention_id = create_resp.data['id']

        # Démarrer
        demarrer_url = reverse('intervention-demarrer', kwargs={'pk': intervention_id})
        assert authenticated_client.post(demarrer_url).status_code == 200

        # Ajouter pièce
        ajout_piece_url = reverse('intervention-ajouter-piece', kwargs={'pk': intervention_id})
        piece_data = {"piece_id": str(piece.id), "quantite": 2}
        assert authenticated_client.post(ajout_piece_url, piece_data, format='json').status_code == 200

        # Terminer
        terminer_url = reverse('intervention-terminer', kwargs={'pk': intervention_id})
        response = authenticated_client.post(terminer_url)
        assert response.status_code == 200
        assert 'cout_total' in response.data

    def test_calculer_cout(self, authenticated_client):
        # Créer un bien
        stock_url = reverse('bien-list')
        bien_resp = authenticated_client.post(stock_url, {
            "reference": "B003", "nom": "Imprimante",
            "prix_unitaire_ht": 300.00, "etat": "disponible"
        }, format='json')
        assert bien_resp.status_code == 201
        bien_id = bien_resp.data['id']

        technicien = TechnicienModel.objects.create(
            nom="Durand", prenom="Paul", email="paul@example.com", cout_horaire=40.0
        )
        piece = PieceDetacheeModel.objects.create(
            reference="P003", nom="Toner", prix_unitaire=50.0, stock=2
        )
        now = timezone.now()
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (now + timedelta(days=1)).isoformat(),
            "date_fin": (now + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        url = reverse('intervention-list')
        create_resp = authenticated_client.post(url, data, format='json')
        assert create_resp.status_code == 201
        intervention_id = create_resp.data['id']

        # Démarrer
        demarrer_url = reverse('intervention-demarrer', kwargs={'pk': intervention_id})
        authenticated_client.post(demarrer_url)

        # Ajouter pièce
        ajout_piece_url = reverse('intervention-ajouter-piece', kwargs={'pk': intervention_id})
        piece_data = {"piece_id": str(piece.id), "quantite": 1}
        authenticated_client.post(ajout_piece_url, piece_data, format='json')

        # Terminer
        terminer_url = reverse('intervention-terminer', kwargs={'pk': intervention_id})
        authenticated_client.post(terminer_url)

        # Vérifier coût
        cout_url = reverse('intervention-cout', kwargs={'pk': intervention_id})
        response = authenticated_client.get(cout_url)
        assert response.status_code == 200
        assert 'cout_total' in response.data
        assert response.data['cout_total'] > 0