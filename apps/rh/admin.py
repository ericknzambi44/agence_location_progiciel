"""
Configuration de l'interface d'administration Django pour le module RH.

Ce fichier enregistre les modèles `Employe`, `Pointage`, `Evaluation` et `Role`
dans l'admin Django, avec des options d'affichage, de recherche, de filtrage
et des protections contre la suppression d'employés possédant déjà
des pointages ou des évaluations.

Note :
    Les noms de modèles sont désormais `Employe`, `Pointage`, `Evaluation` et `Role`
    (anciennement `EmployeModel`, `PointageModel`, etc.).
    Les relations inverses utilisent les `related_name` définis dans les modèles :
        - `Employe.pointages` pour les pointages d'un employé
        - `Employe.evaluations` pour les évaluations d'un employé
"""

from django.contrib import admin
from .infrastructure.models import Employe, Pointage, Evaluation, Role


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    """
    Administration des employés.

    Permet de gérer les informations de base, les rôles (groupes) et
    l'association à un compte utilisateur Django.
    """

    list_display = (
        'matricule',
        'nom',
        'prenom',
        'email',
        'agence',
        'user_account',
        'est_actif'
    )
    search_fields = ('matricule', 'nom', 'prenom', 'email', 'user__username')
    list_filter = ('est_actif', 'agence')
    raw_id_fields = ('user',)
    filter_horizontal = ('groups',)

    @admin.display(description='Utilisateur')
    def user_account(self, obj):
        """
        Affiche le nom d'utilisateur Django associé à l'employé,
        ou un tiret si aucun utilisateur n'est lié.
        """
        return obj.user.username if obj.user else '-'

    def has_delete_permission(self, request, obj=None):
        """
        Empêche la suppression d'un employé s'il possède déjà
        des pointages ou des évaluations enregistrés.

        Utilise les related_names définis dans les modèles :
            - `obj.pointages` (relation inverse vers `Pointage`)
            - `obj.evaluations` (relation inverse vers `Evaluation`)
        """
        if obj and (obj.pointages.exists() or obj.evaluations.exists()):
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    """
    Administration des pointages.

    Permet de visualiser et filtrer les pointages par employé, type et date.
    """

    list_display = ('employe', 'horodatage', 'type')
    list_filter = ('type', 'horodatage')
    search_fields = ('employe__nom', 'employe__prenom', 'employe__matricule')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """
    Administration des évaluations.

    Permet de visualiser et filtrer les évaluations par employé et date.
    """

    list_display = ('employe', 'date_evaluation', 'note')
    list_filter = ('date_evaluation',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Administration des rôles métier.

    Permet de gérer les rôles applicatifs avec leurs permissions JSON.
    """

    list_display = ('nom',)
    search_fields = ('nom',)