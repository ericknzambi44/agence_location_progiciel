from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.statistiques_viewset import StatistiquesViewSet

router = DefaultRouter()
router.register(r'statistiques', StatistiquesViewSet, basename='statistiques')

urlpatterns = [
    path('', include(router.urls)),
]