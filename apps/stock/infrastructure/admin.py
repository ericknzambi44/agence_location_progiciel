from django.contrib import admin
from .models import BienModel, CategorieModel, MouvementStockModel, DisponibilitePeriodeModel

@admin.register(BienModel)
class BienModelAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'etat', 'prix_unitaire_ht')
    search_fields = ('reference', 'nom')

@admin.register(CategorieModel)
class CategorieModelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'parent')
    search_fields = ('nom',)

@admin.register(MouvementStockModel)
class MouvementStockModelAdmin(admin.ModelAdmin):
    list_display = ('bien', 'quantite', 'type_mouvement', 'date_heure')
    list_filter = ('type_mouvement',)

@admin.register(DisponibilitePeriodeModel)
class DisponibilitePeriodeModelAdmin(admin.ModelAdmin):
    list_display = ('bien', 'date_debut', 'date_fin', 'est_reserve')