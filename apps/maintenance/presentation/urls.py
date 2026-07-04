from django.urls import path, include
from rest_framework.routers import DefaultRouter

from maintenance.presentation.views.intervention_viewset import InterventionViewSet

from .views.piece_viewset import PieceDetacheeViewSet
from .views.regle_maintenance_viewset import RegleMaintenanceViewSet
from .views.technicien_viewset import TechnicienViewSet

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')
router.register(r'pieces', PieceDetacheeViewSet, basename='piece')
router.register(r'regles-maintenance', RegleMaintenanceViewSet, basename='regle-maintenance')
router.register(r'techniciens', TechnicienViewSet, basename='technicien')

urlpatterns = [
    path('', include(router.urls)),
]