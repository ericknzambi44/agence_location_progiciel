"""
Configuration de l'interface d'administration Django pour le module Stock.

Enregistre les modèles `Bien`, `Categorie`, `MouvementStock` et
`DisponibilitePeriode` avec des options d'affichage, de recherche,
de filtrage et des libellés français.
"""

from django.contrib import admin
from .infrastructure.models import (
    Bien,
    Categorie,
    MouvementStock,
    DisponibilitePeriode,
)


@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    """
    Administration des biens.
    """

    list_display = ('reference', 'nom', 'etat', 'prix_unitaire_ht', 'devise')
    search_fields = ('reference', 'nom')
    list_filter = ('etat', 'devise')


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """
    Administration des catégories de biens.
    """

    list_display = ('nom', 'parent')
    search_fields = ('nom',)
    list_filter = ('parent',)


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    """
    Administration des mouvements de stock.
    """

    list_display = ('bien', 'quantite', 'type_mouvement', 'date_heure')
    list_filter = ('type_mouvement', 'date_heure')
    search_fields = ('bien__reference', 'bien__nom')


@admin.register(DisponibilitePeriode)
class DisponibilitePeriodeAdmin(admin.ModelAdmin):
    """
    Administration des périodes de disponibilité.
    """

    list_display = ('bien', 'date_debut', 'date_fin', 'est_reserve')
    list_filter = ('est_reserve', 'date_debut', 'date_fin')
    search_fields = ('bien__reference', 'bien__nom')