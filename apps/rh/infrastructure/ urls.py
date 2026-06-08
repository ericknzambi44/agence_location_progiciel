from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rh.presentation.views.rh_viewset import RHViewSet


router = DefaultRouter()
router.register(r'employes', RHViewSet, basename='rh')

urlpatterns = [
    path('', include(router.urls)),
]