from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    register,
    activate,
    CustomTokenObtainPairView,
    UserProfileView,
)

urlpatterns = [
    path('register/', register, name='auth_register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='auth_activate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('me/', UserProfileView.as_view(), name='auth_me'),
]