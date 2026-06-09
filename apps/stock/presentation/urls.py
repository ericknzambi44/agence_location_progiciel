from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.bien_viewset import BienViewSet

router = DefaultRouter()
router.register(r'biens', BienViewSet, basename='bien')

urlpatterns = [
    path('', include(router.urls)),
]