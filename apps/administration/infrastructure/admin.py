from django.contrib import admin
from .models import AgenceModel, ModuleConfigModel

@admin.register(AgenceModel)
class AgenceModelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'actif', 'date_creation')
    search_fields = ('nom', 'ville')
    list_filter = ('actif',)

@admin.register(ModuleConfigModel)
class ModuleConfigModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'active', 'ordre_affichage')
    list_filter = ('active',)