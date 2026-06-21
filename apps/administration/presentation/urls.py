from django.urls import path
from .views.admin_viewset import AdminViewSet

# Mapping des méthodes pour la liste et la création
admin_list = AdminViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Mapping pour le détail, la mise à jour et la suppression
admin_detail = AdminViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Mapping pour les actions personnalisées sur les modules
modules_list = AdminViewSet.as_view({
    'get': 'lister_modules'
})

modules_actifs = AdminViewSet.as_view({
    'get': 'lister_modules_actifs'
})

activer_module = AdminViewSet.as_view({
    'post': 'activer_module'
})

desactiver_module = AdminViewSet.as_view({
    'post': 'desactiver_module'
})

configurer_module = AdminViewSet.as_view({
    'patch': 'configurer_module'
})

urlpatterns = [
    # Route principale : GET et POST sur /admin/
    path('', admin_list, name='admin-list'),

    # Route détail : GET, PUT, PATCH, DELETE sur /admin/<uuid>/
    path('<uuid:pk>/', admin_detail, name='admin-detail'),

    # Actions sur les modules
    path('modules/', modules_list, name='admin-modules'),
    path('modules/actifs/', modules_actifs, name='admin-modules-actifs'),
    path('<uuid:pk>/activer/', activer_module, name='admin-activer'),
    path('<uuid:pk>/desactiver/', desactiver_module, name='admin-desactiver'),
    path('<uuid:pk>/configurer/', configurer_module, name='admin-configurer'),
]