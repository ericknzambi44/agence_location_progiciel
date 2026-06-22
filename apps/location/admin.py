"""
Enregistrement des modèles du module Location dans l'interface d'administration Django.
Permet de gérer les clients et les contrats de location via l'interface admin.
"""
from django.contrib import admin
from location.infrastructure.models import ClientModel, ContratModel


@admin.register(ClientModel)
class ClientModelAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des clients dans l'admin.
    """
    list_display = ('nom', 'prenom', 'email', 'telephone', 'est_actif')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('est_actif',)
    ordering = ('nom', 'prenom')


@admin.register(ContratModel)
class ContratModelAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des contrats dans l'admin.
    """
    list_display = ('id', 'client', 'bien_id', 'date_debut', 'date_fin', 'statut', 'montant_total')
    list_filter = ('statut',)
    search_fields = ('client__nom', 'client__prenom', 'bien_id')
    ordering = ('-date_debut',)



from location.infrastructure.models import RegleTarificationModel

@admin.register(RegleTarificationModel)
class RegleTarificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'agence_id', 'type', 'valeur', 'duree_min', 'active')
    list_filter = ('type', 'active')
    search_fields = ('description',)    