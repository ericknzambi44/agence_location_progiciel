"""
Permissions personnalisées pour le framework REST (DRF).

Gère le contrôle d'accès basé sur les rôles (RBAC) en utilisant
les permissions natives de Django couplées aux rôles/groupes.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveUser(BasePermission):
    """
    Vérifie que l'utilisateur est authentifié et que son compte est actif.
    """

    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.is_active
        )


class HasModulePermission(BasePermission):
    """
    Permission dynamique basée sur la matrice RBAC Django.

    Mappe automatiquement les actions HTTP de DRF vers les permissions Django :
        - GET / HEAD / OPTIONS  -> view_<model>
        - POST                  -> add_<model>
        - PUT / PATCH           -> change_<model>
        - DELETE                -> delete_<model>

    Exige que le ViewSet définisse l'attribut `required_module` ou `queryset`.
    Exemple dans un ViewSet : `required_module = 'rh'`
    """

    # Mapping HTTP -> Verbe de permission Django
    ACTION_MAP = {
        'GET': 'view',
        'OPTIONS': 'view',
        'HEAD': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }

    def has_permission(self, request, view):
        user = request.user

        # 1. Bloquer les utilisateurs non authentifiés ou inactifs
        if not user or not user.is_authenticated or not user.is_active:
            return False

        # 2. Les superusers outrepassent TOUTES les vérifications
        #    (placé AVANT la recherche du module pour garantir le bypass total)
        if user.is_superuser:
            return True

        # 3. Déterminer le nom du module (ex: 'rh', 'stock', 'maintenance')
        module_name = getattr(view, 'required_module', None)
        
        # Si non renseigné explicitement, essayer de le déduire du queryset/modèle
        if not module_name and hasattr(view, 'queryset') and view.queryset is not None:
            module_name = view.queryset.model._meta.app_label

        if not module_name:
            # Sécurité par défaut : si aucun module n'est identifié, refuser l'accès
            return False

        # 4. Déterminer le nom du modèle (nom Django, pas le nom de la classe Python)
        model_name = getattr(view, 'required_model', None)
        if not model_name and hasattr(view, 'queryset') and view.queryset is not None:
            # 🔥 CORRECTION : utiliser _meta.model_name (ex: 'employe', pas 'EmployeModel')
            model_name = view.queryset.model._meta.model_name

        if not model_name:
            return False

        # 5. Déterminer l'action HTTP et le verbe de permission correspondant
        action_verb = self.ACTION_MAP.get(request.method)
        if not action_verb:
            return False

        # 6. Reconstruire la clé de permission Django : "app_label.action_modelname"
        #    Exemple corrigé : "rh.view_employe" (et non "rh.view_employemodel")
        permission_codename = f"{module_name}.{action_verb}_{model_name}"

        # 7. Vérifier si l'utilisateur possède la permission (directe ou via groupe/rôle)
        return user.has_perm(permission_codename)