"""
Définition des URLs du module Location.

Ce module expose les endpoints liés aux clients, contrats, calcul du montant
estimé et gestion des règles de tarification.

Utilisation du routeur DRF pour générer automatiquement les routes.
Les ViewSets sont enregistrés avec un préfixe vide pour LocationViewSet
et 'tarification' pour TarificationViewSet, afin de préserver les chemins existants :
    - /api/location/clients/
    - /api/location/contrats/
    - /api/location/contrats/{uuid}/retourner/
    - /api/location/calculer-montant/
    - /api/location/tarification/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.location_viewset import LocationViewSet
from .views.tarification_viewset import TarificationViewSet

router = DefaultRouter()

# Enregistrement du ViewSet principal de location avec un préfixe vide
# afin que les actions @action (clients, contrats, calculer-montant)
# soient directement accessibles sous /api/location/...
router.register(r'', LocationViewSet, basename='location')

# Enregistrement du ViewSet de tarification sous le préfixe 'tarification'
router.register(r'tarification', TarificationViewSet, basename='tarification')

urlpatterns = [
    path('', include(router.urls)),
]