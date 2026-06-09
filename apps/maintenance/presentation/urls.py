from django.urls import path, include
from maintenance.presentation.views.intervention_viewset import InterventionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')

urlpatterns = [
    path('', include(router.urls)),
]