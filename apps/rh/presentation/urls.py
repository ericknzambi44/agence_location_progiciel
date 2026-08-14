# apps/rh/presentation/urls.py
"""
Configuration des URLs pour le module Ressources Humaines (RH).

Routes exposées :
    - /employes/              : liste et création des employés
    - /employes/actifs/       : liste des employés actifs
    - /pointages/             : enregistrement d'un pointage
    - /employes/<uuid>/pointages/<date>/ : consultation des pointages d'un employé

Note :
    La route /me/ a été déplacée dans le module authentication (/api/auth/me/)
    pour éviter les conflits de permissions et de duplication.
"""

from django.urls import path
from .views.rh_viewset import RHViewSet

urlpatterns = [
    # --------------------------------------------------------------------------
    # Employés
    # --------------------------------------------------------------------------
    path(
        'employes/',
        RHViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='employe-list'
    ),
    path(
        'employes/actifs/',
        RHViewSet.as_view({'get': 'lister_actifs'}),
        name='employe-actifs'
    ),

    # --------------------------------------------------------------------------
    # Pointages
    # --------------------------------------------------------------------------
    path(
        'pointages/',
        RHViewSet.as_view({'post': 'enregistrer_pointage'}),
        name='pointage-create'
    ),
    path(
        'employes/<uuid:pk>/pointages/<str:date_str>/',
        RHViewSet.as_view({'get': 'consulter_pointages'}),
        name='pointages-by-date'
    ),
]