import pytest
import uuid
from django.urls import reverse
from rest_framework import status
from administration.infrastructure.models import ModuleConfigModel

pytestmark = pytest.mark.django_db

class TestAdminAPI:
    @pytest.fixture
    def sample_agence_data(self):
        unique_id = uuid.uuid4().hex[:8]
        return {
            "nom": f"Agence Test {unique_id}",
            "adresse_ligne1": "1 rue de Paris",
            "adresse_ligne2": "",
            "code_postal": "75001",
            "ville": "Paris",
            "pays": "France",
            "telephone": "0123456789",
            "email": f"contact_{unique_id}@agence.fr"
        }

    def test_creer_agence(self, authenticated_client, sample_agence_data):
        url = reverse('admin-list')
        response = authenticated_client.post(url, sample_agence_data, format='json')
        print("\n[DEBUG] test_creer_agence - response.data:", response.data)
        assert response.status_code == status.HTTP_201_CREATED, f"Erreur: {response.data}"

    def test_lister_agences(self, authenticated_client, sample_agence_data):
        url = reverse('admin-list')
        authenticated_client.post(url, sample_agence_data, format='json')
        agences_url = reverse('admin-agences')
        response = authenticated_client.get(agences_url)
        assert response.status_code == 200

    def test_lister_modules(self, authenticated_client):
        ModuleConfigModel.objects.create(code="STOCK", nom="Stock")
        url = reverse('admin-modules')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_activer_module(self, authenticated_client):
     module = ModuleConfigModel.objects.create(code="RH1", nom="Ressources Humaines", active=False)
     url = reverse('admin-activer-module', args=[module.id])
     response = authenticated_client.post(url)
     assert response.status_code == 200
     module.refresh_from_db()
     assert module.active is True