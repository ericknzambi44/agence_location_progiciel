"""
Routage de l'API - Module Stock.

Définit l'exposition HTTP des endpoints du module Stock via le router DRF.
Les routes générées s'interfacent avec les ViewSets sécurisés par RBAC :

    - BienViewSet    -> /api/stock/biens/
    - StockViewSet   -> /api/stock/stock/

Exemples d'endpoints :
    GET    /api/stock/biens/                         -> Liste des biens
    POST   /api/stock/biens/                         -> Création d'un bien
    GET    /api/stock/biens/{uuid}/                  -> Détail d'un bien
    PATCH  /api/stock/biens/{uuid}/changer_etat/     -> Changement d'état
    GET    /api/stock/biens/disponibles/             -> Biens disponibles sur période

    GET    /api/stock/stock/                         -> Niveaux de stock
    POST   /api/stock/stock/                         -> Création d'un mouvement
    GET    /api/stock/stock/{uuid}/niveau/           -> Niveau d'un article
    GET    /api/stock/stock/mouvements/              -> Historique des mouvements
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from stock.presentation.views.bien_viewset import BienViewSet
from stock.presentation.views.stock_viewset import StockViewSet

router = DefaultRouter()
router.register(r'biens', BienViewSet, basename='bien')
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]