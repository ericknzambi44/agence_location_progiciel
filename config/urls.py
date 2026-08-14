"""
Configuration des URLs principales du projet.

Routes importantes :
    - /admin/                : interface d'administration Django
    - /api/stock/            : API module Stock
    - /api/maintenance/      : API module Maintenance
    - /api/rh/               : API module RH
    - /api/admin/            : API module Administration
    - /api-token-auth/       : obtention de token (SimpleJWT)
    - /api/auth/             : authentification (login, register, etc.)
    - /api/location/         : API module Location
    - /api/statistiques/     : API module Statistiques
    - /api/debug-agence/     : vue de debug pour vérifier l'agence
    - /sync-rbac/            : vue de synchronisation des permissions RBAC
                              (protégée par staff_member_required)
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from authentication.views import sync_rbac_admin_view


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_agence(request):
    """
    Vue de debug pour vérifier l'agence associée à l'utilisateur connecté.
    Retourne le nom d'utilisateur, l'email et l'agence_id (si disponible).
    """
    return JsonResponse({
        'user': request.user.username,
        'email': request.user.email,
        'agence_id': str(getattr(request, 'agence_id', None))
    })


urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # API des différents modules
    path('api/stock/', include('stock.presentation.urls')),
    path('api/maintenance/', include('maintenance.presentation.urls')),
    path('api/rh/', include('rh.presentation.urls')),
    path('api/admin/', include('administration.presentation.urls')),

    # Endpoint d'authentification par token
    path('api-token-auth/', token_views.obtain_auth_token),

    # Authentification JWT (login, register, refresh, me)
    path('api/auth/', include('authentication.urls')),

    # Autres APIs
    path('api/location/', include('location.presentation.urls')),
    path('api/statistiques/', include('statistiques.presentation.urls')),

    # Vue de debug pour l'agence
    path('api/debug-agence/', debug_agence, name='debug-agence'),

    # Vue de synchronisation RBAC (protégée par staff_member_required)
    # NOTE : placée hors du préfixe /admin/ pour éviter le conflit avec
    # l'AdminSite de Django (qui intercepte tout /admin/...).
    path('sync-rbac/', sync_rbac_admin_view, name='sync_rbac'),
]