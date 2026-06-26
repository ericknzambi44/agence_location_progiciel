"""
Définition des URLs du module Location.
Regroupe les endpoints pour les clients, les contrats, le calcul du montant
et la gestion des règles de tarification.
"""
from django.urls import path
from .views.location_viewset import LocationViewSet
from .views.tarification_viewset import TarificationViewSet

# Instanciation des ViewSets pour le mapping des méthodes
location_view = LocationViewSet.as_view
tarif_view = TarificationViewSet.as_view({
    'get': 'list',    # GET /tarification/ → consulter les règles
    'post': 'create'  # POST /tarification/ → configurer les règles
})

urlpatterns = [
    # ---- Clients ----
    path('clients/',
         location_view({'get': 'list_clients', 'post': 'create_client'}),
         name='client-list'),

    # ---- Contrats ----
    path('contrats/',
         location_view({'get': 'list_contrats', 'post': 'create_contrat'}),
         name='contrat-list'),
    path('contrats/<uuid:pk>/retourner/',
         location_view({'post': 'retourner'}),
         name='contrat-retourner'),

    # ---- Calcul du montant estimé ----
    path('calculer-montant/',
         location_view({'post': 'calculer_montant'}),
         name='calculer-montant'),


     path('contrats/<uuid:pk>/', location_view({'get': 'retrieve'}), name='contrat-detail'),    

    # ---- Gestion des règles de tarification ----
    path('tarification/',
         tarif_view,
         name='tarification'),
]