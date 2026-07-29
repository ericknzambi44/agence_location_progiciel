"""
Routage de l'API - Module Stock.

Définit l'exposition HTTP des endpoints du module Stock via le router DRF.
Les routes générées s'interfacent avec le BienViewSet sécurisé par RBAC.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from stock.presentation.views.bien_viewset import BienViewSet

router = DefaultRouter()
router.register(r'biens', BienViewSet, basename='bien')

urlpatterns = [
    path('', include(router.urls)),
]