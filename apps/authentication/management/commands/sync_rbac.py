"""
Commande de management : synchronisation des permissions RBAC.

Cette commande est idempotente et autonome :
- Elle crée les ContentTypes manquants pour tous les modèles des applications métier.
- Elle crée les permissions standard (add, change, delete, view) pour chaque modèle.
- Elle crée les groupes de rôles par défaut et leur assigne les permissions.

Utilisation :
    python manage.py sync_rbac
    python manage.py sync_rbac --create-groups
"""

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Synchronise les permissions RBAC et crée les rôles par défaut."

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-groups',
            action='store_true',
            dest='create_groups',
            help="Crée les groupes de rôles par défaut (RH, Stock, Maintenance, SuperAdmin).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("--- Synchronisation RBAC ---"))

        # 1. Créer les ContentTypes et permissions pour tous les modèles métier
        self.stdout.write("\n[1/2] Création des ContentTypes et permissions...")
        for app_config in apps.get_app_configs():
            # Ignorer les apps non métier
            if app_config.name.startswith('django.') or app_config.name.startswith('rest_framework'):
                continue
            if not app_config.models:
                continue

            for model in app_config.get_models():
                ct, created = ContentType.objects.get_or_create(
                    app_label=model._meta.app_label,
                    model=model._meta.model_name,
                )
                for action in ['add', 'change', 'delete', 'view']:
                    codename = f"{action}_{model._meta.model_name}"
                    name = f"Can {action} {model._meta.verbose_name}"
                    Permission.objects.get_or_create(
                        content_type=ct,
                        codename=codename,
                        defaults={'name': name[:255]}
                    )
            self.stdout.write(self.style.SUCCESS(f"  ✔ {app_config.label} : ContentTypes et permissions synchronisés"))

        # 2. Créer les groupes de rôles par défaut (option --create-groups)
        if options['create_groups']:
            self.stdout.write("\n[2/2] Création des groupes de rôles par défaut...")
            self.create_default_groups()
        else:
            self.stdout.write("\n[2/2] Option --create-groups non fournie, groupes ignorés.")

        self.stdout.write(self.style.SUCCESS("\n✅ Synchronisation RBAC terminée."))

    def _assign_permissions_for_app(self, group, app_label):
        """
        Ajoute au groupe toutes les permissions de l'application donnée.
        """
        perms = Permission.objects.filter(content_type__app_label=app_label)
        group.permissions.add(*perms)
        return perms.count()

    def create_default_groups(self):
        """
        Crée les groupes et leur assigne les permissions selon les applications.
        """
        role_config = {
            "Chef d'Agence RH": ['rh'],
            "Gestionnaire Stock": ['stock'],
            "Technicien Maintenance": ['maintenance'],
            "Location Manager": ['location'],
        }

        for group_name, app_labels in role_config.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()
            total = 0
            for app_label in app_labels:
                try:
                    count = self._assign_permissions_for_app(group, app_label)
                    total += count
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  ⚠ {app_label} : {e}"))
            self.stdout.write(f"  ✔ Groupe '{group_name}' : {total} permission(s) assignée(s).")

        # SuperAdmin : toutes les permissions
        super_group, _ = Group.objects.get_or_create(name="SuperAdmin")
        super_group.permissions.set(Permission.objects.all())
        self.stdout.write(f"  ✔ Groupe 'SuperAdmin' : {super_group.permissions.count()} permission(s) assignée(s).")


        #commande pour créer les groupes par défaut : python manage.py sync_rbac --create-groups