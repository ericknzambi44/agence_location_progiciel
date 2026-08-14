"""
Enregistrement des modèles du module Location dans l'interface d'administration Django.

Permet de gérer les clients, les contrats de location et les règles de
tarification via l'interface admin.

Les modèles sont enregistrés sous leurs nouveaux noms (sans suffixe "Model") :
    - Client
    - Contrat
    - RegleTarification
"""

from django.contrib import admin
from location.infrastructure.models import Client, Contrat, RegleTarification


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des clients dans l'admin.
    """

    list_display = ('nom', 'prenom', 'email', 'telephone', 'agence', 'est_actif')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('est_actif', 'agence')
    ordering = ('nom', 'prenom')


@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des contrats dans l'admin.
    """

    list_display = (
        'id',
        'client',
        'bien_id',
        'date_debut',
        'date_fin',
        'statut',
        'montant_total',
        'agence',
    )
    list_filter = ('statut', 'agence')
    search_fields = ('client__nom', 'client__prenom', 'bien_id')
    ordering = ('-date_debut',)


@admin.register(RegleTarification)
class RegleTarificationAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des règles de tarification dans l'admin.
    """

    list_display = (
        'id',
        'agence',
        'type',
        'valeur',
        'duree_min',
        'duree_max',
        'active',
    )
    list_filter = ('type', 'active', 'agence')
    search_fields = ('description',)