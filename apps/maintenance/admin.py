# maintenance/admin.py
from django.contrib import admin
from maintenance.infrastructure.models import (
    TechnicienModel,
    PieceDetacheeModel,
    InterventionModel,
    InterventionPieceModel,
    RegleMaintenanceModel,  # <-- ajout
)

@admin.register(TechnicienModel)
class TechnicienModelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'cout_horaire')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(PieceDetacheeModel)
class PieceDetacheeModelAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'prix_unitaire', 'stock')
    search_fields = ('reference', 'nom')

@admin.register(InterventionModel)
class InterventionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'bien_id', 'technicien', 'date_debut', 'date_fin', 'statut')
    list_filter = ('statut',)
    search_fields = ('bien_id', 'technicien__nom')

@admin.register(InterventionPieceModel)
class InterventionPieceModelAdmin(admin.ModelAdmin):
    list_display = ('intervention', 'piece', 'quantite')
    list_filter = ('intervention__statut',)

@admin.register(RegleMaintenanceModel)  # <-- ajout
class RegleMaintenanceModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'agence_id', 'type', 'valeur', 'duree_min', 'duree_max', 'active')
    list_filter = ('type', 'active')
    search_fields = ('description',)