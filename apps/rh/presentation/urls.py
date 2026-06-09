from django.urls import path
from .views.rh_viewset import RHViewSet

urlpatterns = [
    path('employes/', RHViewSet.as_view({'get': 'list', 'post': 'create'}), name='employe-list'),
    path('employes/actifs/', RHViewSet.as_view({'get': 'lister_actifs'}), name='employe-actifs'),
    path('pointages/', RHViewSet.as_view({'post': 'enregistrer_pointage'}), name='pointage-create'),
    path('employes/<uuid:pk>/pointages/<str:date_str>/', RHViewSet.as_view({'get': 'consulter_pointages'}), name='pointages-by-date'),
]