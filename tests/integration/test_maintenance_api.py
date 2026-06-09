import pytest
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from maintenance.infrastructure.models import TechnicienModel, PieceDetacheeModel

pytestmark = pytest.mark.django_db

class TestMaintenanceAPI:
    def test_planifier_intervention(self, authenticated_client):
        # 1. Créer un bien via l'API Stock
        stock_url = reverse('bien-list')
        bien_data = {
            "reference": "B001",
            "nom": "Ordinateur",
            "prix_unitaire_ht": 1200.00,
            "etat": "disponible"
        }
        bien_resp = authenticated_client.post(stock_url, bien_data, format='json')
        assert bien_resp.status_code == status.HTTP_201_CREATED
        bien_id = bien_resp.data['id']

        # 2. Créer un technicien via le modèle (pas d'API dédiée pour l'instant)
        technicien = TechnicienModel.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            cout_horaire=25.0
        )

        # 3. Planifier l'intervention
        url = reverse('intervention-list')
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (datetime.now() + timedelta(days=1)).isoformat(),
            "date_fin": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['statut'] == 'planifiee'

    def test_ajouter_piece_et_terminer(self, authenticated_client):
        # 1. Créer un bien via l'API Stock
        stock_url = reverse('bien-list')
        bien_data = {
            "reference": "B002",
            "nom": "Ordinateur",
            "prix_unitaire_ht": 1200.00,
            "etat": "disponible"
        }
        bien_resp = authenticated_client.post(stock_url, bien_data, format='json')
        assert bien_resp.status_code == status.HTTP_201_CREATED
        bien_id = bien_resp.data['id']

        # 2. Créer un technicien
        technicien = TechnicienModel.objects.create(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            cout_horaire=30.0
        )

        # 3. Créer une pièce détachée
        piece = PieceDetacheeModel.objects.create(
            reference="P002",
            nom="Clavier",
            prix_unitaire=15.0,
            stock=5
        )

        # 4. Planifier l'intervention
        url = reverse('intervention-list')
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (datetime.now() + timedelta(days=1)).isoformat(),
            "date_fin": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        create_resp = authenticated_client.post(url, data, format='json')
        assert create_resp.status_code == status.HTTP_201_CREATED
        intervention_id = create_resp.data['id']

        # 5. Démarrer l'intervention
        demarrer_url = reverse('intervention-demarrer', kwargs={'pk': intervention_id})
        response = authenticated_client.post(demarrer_url)
        assert response.status_code == 200

        # 6. Ajouter une pièce
        ajout_piece_url = reverse('intervention-ajouter-piece', kwargs={'pk': intervention_id})
        piece_data = {"piece_id": str(piece.id), "quantite": 2}
        response = authenticated_client.post(ajout_piece_url, piece_data, format='json')
        assert response.status_code == 200

        # 7. Terminer l'intervention
        terminer_url = reverse('intervention-terminer', kwargs={'pk': intervention_id})
        response = authenticated_client.post(terminer_url)
        assert response.status_code == 200
        assert 'cout_total' in response.data

    def test_calculer_cout(self, authenticated_client):
        # 1. Créer un bien via l'API Stock
        stock_url = reverse('bien-list')
        bien_data = {
            "reference": "B003",
            "nom": "Imprimante",
            "prix_unitaire_ht": 300.00,
            "etat": "disponible"
        }
        bien_resp = authenticated_client.post(stock_url, bien_data, format='json')
        assert bien_resp.status_code == status.HTTP_201_CREATED
        bien_id = bien_resp.data['id']

        # 2. Créer un technicien
        technicien = TechnicienModel.objects.create(
            nom="Durand",
            prenom="Paul",
            email="paul@example.com",
            cout_horaire=40.0
        )

        # 3. Créer une pièce
        piece = PieceDetacheeModel.objects.create(
            reference="P003",
            nom="Toner",
            prix_unitaire=50.0,
            stock=2
        )

        # 4. Planifier l'intervention
        url = reverse('intervention-list')
        data = {
            "bien_id": bien_id,
            "technicien_id": str(technicien.id),
            "date_debut": (datetime.now() + timedelta(days=1)).isoformat(),
            "date_fin": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
            "description_panne": "Test panne"
        }
        create_resp = authenticated_client.post(url, data, format='json')
        assert create_resp.status_code == status.HTTP_201_CREATED
        intervention_id = create_resp.data['id']

        # 5. Démarrer
        demarrer_url = reverse('intervention-demarrer', kwargs={'pk': intervention_id})
        authenticated_client.post(demarrer_url)

        # 6. Ajouter pièce
        ajout_piece_url = reverse('intervention-ajouter-piece', kwargs={'pk': intervention_id})
        piece_data = {"piece_id": str(piece.id), "quantite": 1}
        authenticated_client.post(ajout_piece_url, piece_data, format='json')

        # 7. Terminer
        terminer_url = reverse('intervention-terminer', kwargs={'pk': intervention_id})
        authenticated_client.post(terminer_url)

        # 8. Vérifier le coût
        cout_url = reverse('intervention-cout', kwargs={'pk': intervention_id})
        response = authenticated_client.get(cout_url)
        assert response.status_code == 200
        assert 'cout_total' in response.data
        assert response.data['cout_total'] > 0