"""
Routage de l'API - Module Maintenance.

Définit l'exposition HTTP des endpoints du module Maintenance via le router DRF.
Les routes générées s'interfacent avec les ViewSets sécurisés par RBAC :

    - InterventionViewSet        -> /api/maintenance/interventions/
    - PieceDetacheeViewSet       -> /api/maintenance/pieces/
    - RegleMaintenanceViewSet    -> /api/maintenance/regles-maintenance/
    - TechnicienViewSet          -> /api/maintenance/techniciens/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from maintenance.presentation.views.intervention_viewset import InterventionViewSet
from maintenance.presentation.views.piece_detachee_viewset import PieceDetacheeViewSet
from maintenance.presentation.views.regle_maintenance_viewset import RegleMaintenanceViewSet
from maintenance.presentation.views.technicien_viewset import TechnicienViewSet

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')
router.register(r'pieces', PieceDetacheeViewSet, basename='piece')
router.register(r'regles-maintenance', RegleMaintenanceViewSet, basename='regle-maintenance')
router.register(r'techniciens', TechnicienViewSet, basename='technicien')

urlpatterns = [
    path('', include(router.urls)),
]