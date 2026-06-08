from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.maintenance.presentation.serializers.views.intervention_viewset import InterventionViewSet
InterventionViewSet

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')

urlpatterns = [
    path('', include(router.urls)),
]