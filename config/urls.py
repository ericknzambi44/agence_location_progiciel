from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stock/', include('stock.presentation.urls')),
    path('api/maintenance/', include('maintenance.presentation.urls')),
    path('api/rh/', include('rh.presentation.urls')),
    path('api/admin/', include('administration.presentation.urls')),
    path('api-token-auth/', token_views.obtain_auth_token),  # endpoint pour obtenir token
    path('api/auth/', include('authentication.urls')),
    path('api/location/', include('location.presentation.urls')),
    
]