"""
Commande de management Django : Initialisation des Rôles et Permissions RBAC.
Génère à la volée les permissions manquantes dans auth_permission si nécessaire.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

try:
    from rh.infrastructure.models import (
        EmployeModel,
        PointageModel,
        EvaluationModel,
        RoleModel,
    )
    from stock.infrastructure.models import (
        CategorieModel,
        BienModel,
        MouvementStockModel,
        DisponibilitePeriodeModel,
    )
    from maintenance.infrastructure.models import (
        TechnicienModel,
        PieceDetacheeModel,
        InterventionModel,
        InterventionPieceModel,
        RegleMaintenanceModel,
    )
except ModuleNotFoundError:
    from apps.rh.infrastructure.models import (
        EmployeModel,
        PointageModel,
        EvaluationModel,
        RoleModel,
    )
    from apps.stock.infrastructure.models import (
        CategorieModel,
        BienModel,
        MouvementStockModel,
        DisponibilitePeriodeModel,
    )
    from apps.maintenance.infrastructure.models import (
        TechnicienModel,
        PieceDetacheeModel,
        InterventionModel,
        InterventionPieceModel,
        RegleMaintenanceModel,
    )


class Command(BaseCommand):
    help = "Initialise les rôles et génère/associe les permissions RBAC."

    def get_or_create_permission(self, content_type, action, model_cls):
        """
        Récupère la permission ou la crée explicitement en BDD si Django ne l'a pas générée.
        """
        model_name = model_cls._meta.model_name
        verbose_name = model_cls._meta.verbose_name
        codename = f"{action}_{model_name}"
        
        action_labels = {
            'add': 'Can add',
            'change': 'Can change',
            'delete': 'Can delete',
            'view': 'Can view',
        }
        label = action_labels.get(action, f"Can {action}")
        name = f"{label} {verbose_name}"

        perm, created = Permission.objects.get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={'name': name[:255]}
        )
        if created:
            self.stdout.write(
                self.style.WARNING(f"  📌 Permission générée en BDD : {codename}")
            )
        return perm

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("--- Initialisation des Rôles RBAC ---"))

        roles_config = {
            "Chef d'Agence RH": [
                (EmployeModel, ['add', 'change', 'delete', 'view']),
                (PointageModel, ['add', 'change', 'delete', 'view']),
                (EvaluationModel, ['add', 'change', 'delete', 'view']),
                (RoleModel, ['add', 'change', 'delete', 'view']),
                (BienModel, ['view']),
                (CategorieModel, ['view']),
            ],
            "Gestionnaire Stock": [
                (BienModel, ['add', 'change', 'delete', 'view']),
                (CategorieModel, ['add', 'change', 'delete', 'view']),
                (MouvementStockModel, ['add', 'change', 'delete', 'view']),
                (DisponibilitePeriodeModel, ['add', 'change', 'delete', 'view']),
            ],
            "Technicien Maintenance": [
                (TechnicienModel, ['add', 'change', 'delete', 'view']),
                (PieceDetacheeModel, ['add', 'change', 'delete', 'view']),
                (InterventionModel, ['add', 'change', 'delete', 'view']),
                (InterventionPieceModel, ['add', 'change', 'delete', 'view']),
                (RegleMaintenanceModel, ['add', 'change', 'delete', 'view']),
                (BienModel, ['change', 'view']),
            ],
        }

        for role_name, mappings in roles_config.items():
            group, created = Group.objects.get_or_create(name=role_name)
            status_txt = "Créé" if created else "Existant"
            self.stdout.write(f"\n[Rôle] {role_name} ({status_txt})")

            group.permissions.clear()
            assigned_count = 0

            for model_cls, actions in mappings:
                content_type = ContentType.objects.get_for_model(model_cls)

                for action in actions:
                    perm = self.get_or_create_permission(content_type, action, model_cls)
                    group.permissions.add(perm)
                    assigned_count += 1

            self.stdout.write(self.style.SUCCESS(f"  -> {assigned_count} permission(s) affectée(s)."))

        # SuperAdmin
        super_admin_group, _ = Group.objects.get_or_create(name="SuperAdmin")
        all_permissions = Permission.objects.all()
        super_admin_group.permissions.set(all_permissions)
        self.stdout.write(
            self.style.SUCCESS(
                f"\n[Rôle] SuperAdmin -> Toutes les permissions du système ({all_permissions.count()}) assignées."
            )
        )

        self.stdout.write(
            self.style.SUCCESS("\n✅ Initialisation RBAC terminée avec succès !")
        )