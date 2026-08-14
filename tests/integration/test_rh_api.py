"""
Tests d'intégration pour l'API RH.

Ce module contient des tests pour les endpoints principaux du module RH :
    - Création d'un employé (POST /api/rh/employes/)
    - Liste des employés actifs (GET /api/rh/employes/actifs/)
    - Enregistrement d'un pointage (POST /api/rh/pointages/)
    - Consultation des pointages (GET /api/rh/employes/{id}/pointages/YYYY-MM-DD/)
"""

import pytest
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from rh.infrastructure.models import Employe  # ✅ Correction : EmployeModel -> Employe
from tests.conftest import authenticated_client

pytestmark = pytest.mark.django_db


class TestRHAPI:
    """
    Tests d'intégration pour le module RH.
    """

    @pytest.fixture
    def sample_employe_data(self):
        """
        Données minimales valides pour créer un employé.
        """
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
        """
        Vérifie que la création d'un employé fonctionne.
        """
        url = reverse('employe-list')
        response = authenticated_client.post(url, sample_employe_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['matricule'] == sample_employe_data['matricule']

    def test_lister_employes_actifs(self, authenticated_client, sample_employe_data):
        """
        Vérifie que la liste des employés actifs retourne au moins l'employé créé.
        """
        url = reverse('employe-list')
        authenticated_client.post(url, sample_employe_data, format='json')

        actifs_url = reverse('employe-actifs')
        response = authenticated_client.get(actifs_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_enregistrer_pointage(self, authenticated_client, sample_employe_data):
        """
        Vérifie que l'enregistrement d'un pointage pour un employé existant fonctionne.
        """
        create_url = reverse('employe-list')
        create_resp = authenticated_client.post(create_url, sample_employe_data, format='json')
        employe_id = create_resp.data['id']

        # Le nom d'URL pour l'action personnalisée 'pointages' dépend du basename du routeur.
        # Ici on suppose que le routeur est enregistré avec basename='employe',
        # et que l'action personnalisée 'pointages' est accessible via 'employe-pointages'.
        pointage_url = reverse('employe-pointages')
        data = {
            "employe_id": employe_id,
            "type": "ENTRY",
            "horodatage": datetime.now().isoformat()
        }
        response = authenticated_client.post(pointage_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_consulter_pointages(self, authenticated_client, sample_employe_data):
        """
        Vérifie que la consultation des pointages d'un employé pour une date donnée fonctionne.
        """
        # Créer un employé
        create_url = reverse('employe-list')
        create_resp = authenticated_client.post(create_url, sample_employe_data, format='json')
        employe_id = create_resp.data['id']

        # Enregistrer un pointage
        pointage_url = reverse('employe-pointages')
        data = {
            "employe_id": employe_id,
            "type": "ENTRY",
            "horodatage": datetime.now().isoformat()
        }
        authenticated_client.post(pointage_url, data, format='json')

        # Construire l'URL de consultation avec la date du pointage
        pointage_date = datetime.now().strftime('%Y-%m-%d')
        # L'action personnalisée 'consulter_pointages' a un paramètre date_str dans l'URL.
        # On suppose que le nom d'URL est 'employe-pointages-date' (ou similaire).
        # Il faudra adapter selon la configuration réelle des URLs.
        # Par exemple : reverse('employe-pointages-date', kwargs={'pk': employe_id, 'date_str': pointage_date})
        # Ici, on utilise la convention de nommage DRF pour les actions detail.
        url = reverse('employe-pointages-date', kwargs={'pk': employe_id, 'date_str': pointage_date})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1