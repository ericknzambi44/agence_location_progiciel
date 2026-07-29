import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date, datetime
from uuid import uuid4
from rh.infrastructure.models import EmployeModel
from tests.conftest import authenticated_client

pytestmark = pytest.mark.django_db

class TestRHAPI:
    @pytest.fixture
    def sample_employe_data(self):
        return {
            "matricule": "EMP001",
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean@example.com",
            "date_embauche": "2025-01-01",
            "taux_horaire": 25.50,
            "poste": "Technicien"
        }

    def test_embaucher_employe(self, authenticated_client, sample_employe_data):
     url = reverse('employe-list')
     response = authenticated_client.post(url, sample_employe_data, format='json')
     assert response.status_code == status.HTTP_201_CREATED
   
     assert response.data['matricule'] == sample_employe_data['matricule']

    def test_lister_employes_actifs(self, authenticated_client, sample_employe_data):
        url = reverse('employe-list')
        authenticated_client.post(url, sample_employe_data, format='json')
        actifs_url = reverse('employe-actifs')
        response = authenticated_client.get(actifs_url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_enregistrer_pointage(self, authenticated_client, sample_employe_data):
        create_url = reverse('employe-list')
        create_resp = authenticated_client.post(create_url, sample_employe_data, format='json')
        employe_id = create_resp.data['id']
        pointage_url = reverse('pointage-create') 
        data = {
            "employe_id": employe_id,
            "type": "ENTRY",
            "horodatage": datetime.now().isoformat()
        }
        response = authenticated_client.post(pointage_url, data, format='json')
        assert response.status_code == 201

    def test_consulter_pointages(self, authenticated_client, sample_employe_data):
        # Créer employé, ajouter pointage, puis consulter
        pass