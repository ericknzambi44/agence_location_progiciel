from django.urls import path, include
from maintenance.presentation.views.intervention_viewset import InterventionViewSet
from rest_framework.routers import DefaultRouter
from maintenance.presentation.views.piece_viewset import PieceDetacheeViewSet

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')
router.register(r'pieces', PieceDetacheeViewSet, basename='piece')

urlpatterns = [
    path('', include(router.urls)),
]