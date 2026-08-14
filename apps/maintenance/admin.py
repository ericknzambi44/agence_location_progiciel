"""
Configuration de l'interface d'administration Django pour le module Maintenance.

Enregistre les modèles renommés sans suffixe "Model" :
    - Technicien
    - PieceDetachee
    - Intervention
    - InterventionPiece
    - RegleMaintenance

Chaque classe d'administration offre des options de recherche, filtrage et affichage.
"""

from django.contrib import admin
from maintenance.infrastructure.models import (
    Technicien,
    PieceDetachee,
    Intervention,
    InterventionPiece,
    RegleMaintenance,
)


@admin.register(Technicien)
class TechnicienAdmin(admin.ModelAdmin):
    """
    Administration des techniciens de maintenance.
    """

    list_display = ('nom', 'prenom', 'email', 'cout_horaire')
    search_fields = ('nom', 'prenom', 'email')


@admin.register(PieceDetachee)
class PieceDetacheeAdmin(admin.ModelAdmin):
    """
    Administration des pièces détachées.
    """

    list_display = ('reference', 'nom', 'prix_unitaire', 'stock')
    search_fields = ('reference', 'nom')


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    """
    Administration des interventions.
    """

    list_display = ('id', 'bien_id', 'technicien', 'date_debut', 'date_fin', 'statut')
    list_filter = ('statut',)
    search_fields = ('bien_id', 'technicien__nom')


@admin.register(InterventionPiece)
class InterventionPieceAdmin(admin.ModelAdmin):
    """
    Administration des pièces utilisées dans les interventions.
    """

    list_display = ('intervention', 'piece', 'quantite')
    list_filter = ('intervention__statut',)


@admin.register(RegleMaintenance)
class RegleMaintenanceAdmin(admin.ModelAdmin):
    """
    Administration des règles de tarification de maintenance.
    """

    list_display = ('id', 'agence_id', 'type', 'valeur', 'duree_min', 'duree_max', 'active')
    list_filter = ('type', 'active')
    search_fields = ('description',)