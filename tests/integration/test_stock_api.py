import pytest
import uuid
import time
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

class TestStockAPI:
    @pytest.fixture
    def unique_bien_data(self, sample_bien_data):
     data = sample_bien_data.copy()
    # Utilise un UUID complet pour être sûr
     data['reference'] = f"B{uuid.uuid4().hex.upper()}"
     return data

    def test_creer_bien(self, authenticated_client, unique_bien_data):
        url = reverse('bien-list')
        response = authenticated_client.post(url, unique_bien_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        # La référence est normalisée en majuscules par le Value Object
        assert response.data['reference'] == unique_bien_data['reference'].upper()

    def test_liste_biens(self, authenticated_client, unique_bien_data):
        url = reverse('bien-list')
        authenticated_client.post(url, unique_bien_data, format='json')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_detail_bien(self, authenticated_client, unique_bien_data):
        create_url = reverse('bien-list')
        create_resp = authenticated_client.post(create_url, unique_bien_data, format='json')
        bien_id = create_resp.data['id']
        detail_url = reverse('bien-detail', kwargs={'pk': bien_id})
        response = authenticated_client.get(detail_url)
        assert response.status_code == 200
        assert response.data['reference'] == unique_bien_data['reference'].upper()

    def test_verifier_disponibilite(self, authenticated_client, unique_bien_data):
        url = reverse('bien-list')
        authenticated_client.post(url, unique_bien_data, format='json')
        disponibilite_url = reverse('bien-disponibles')
        response = authenticated_client.get(disponibilite_url, {'debut': '2025-01-01', 'fin': '2025-01-10'})
        assert response.status_code == 200
        # On attend au moins un bien (celui créé)
        assert len(response.data) == 1

    def test_changer_etat(self, authenticated_client, unique_bien_data):
        create_url = reverse('bien-list')
        create_resp = authenticated_client.post(create_url, unique_bien_data, format='json')
        bien_id = create_resp.data['id']
        changer_url = reverse('bien-changer-etat', kwargs={'pk': bien_id})
        response = authenticated_client.patch(changer_url, {'etat': 'en_maintenance'}, format='json')
        assert response.status_code == 200
        detail_url = reverse('bien-detail', kwargs={'pk': bien_id})
        detail = authenticated_client.get(detail_url)
        assert detail.data['etat'] == 'en_maintenance'