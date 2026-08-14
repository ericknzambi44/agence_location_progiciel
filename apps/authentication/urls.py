# apps/authentication/urls.py
"""
URLs du module d'authentification.

Routes exposées :
    - /register/                  : création d'un compte utilisateur
    - /activate/<uidb64>/<token>/ : activation du compte par email
    - /login/                     : connexion (JWT)
    - /refresh/                   : rafraîchissement du token
    - /me/                        : profil complet de l'utilisateur connecté
    - /admin/sync-rbac/           : vue d'administration pour synchroniser RBAC
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    register,
    activate,
    CustomTokenObtainPairView,
    UserProfileView,
    sync_rbac_admin_view,   # <-- Vue admin RBAC
)

urlpatterns = [
    path('register/', register, name='auth_register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='auth_activate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('me/', UserProfileView.as_view(), name='auth_me'),
    # Vue d'administration RBAC (protégée par staff_member_required)
   # path('admin/sync-rbac/', sync_rbac_admin_view, name='sync_rbac'),
]