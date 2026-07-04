from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Vue de debug temporaire pour vérifier l'agence_id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_agence(request):
    return JsonResponse({
        'user': request.user.username,
        'email': request.user.email,
        'agence_id': str(getattr(request, 'agence_id', None))
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stock/', include('stock.presentation.urls')),
    path('api/maintenance/', include('maintenance.presentation.urls')),
    path('api/rh/', include('rh.presentation.urls')),
    path('api/admin/', include('administration.presentation.urls')),
    path('api-token-auth/', token_views.obtain_auth_token),  # endpoint pour obtenir token
    path('api/auth/', include('authentication.urls')),
    path('api/location/', include('location.presentation.urls')),
    path('api/statistiques/', include('statistiques.presentation.urls')),
    path('api/debug-agence/', debug_agence, name='debug-agence'),  # temporaire
]