import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(username='testuser', password='testpass')
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def sample_bien_data():
    return {
        "reference": "B001",
        "nom": "Ordinateur",
        "description": "PC portable",
        "prix_unitaire_ht": 1200.00,
        "date_achat": "2024-01-01"
    }