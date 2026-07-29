"""
Commande de management Django : Génération des utilisateurs de test RBAC.
Crée des utilisateurs de test et leur assigne leurs groupes/rôles respectifs.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = "Crée des utilisateurs de test pour valider le système RBAC."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("--- Création des Utilisateurs de Test RBAC ---"))

        test_users_data = [
            {
                "username": "rh_user",
                "email": "rh@agence.local",
                "password": "password123",
                "role": "Chef d'Agence RH",
            },
            {
                "username": "stock_user",
                "email": "stock@agence.local",
                "password": "password123",
                "role": "Gestionnaire Stock",
            },
            {
                "username": "tech_user",
                "email": "tech@agence.local",
                "password": "password123",
                "role": "Technicien Maintenance",
            },
            {
                "username": "admin_user",
                "email": "admin@agence.local",
                "password": "password123",
                "role": "SuperAdmin",
            },
        ]

        for data in test_users_data:
            role_name = data["role"]
            try:
                group = Group.objects.get(name=role_name)
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"  ❌ Le groupe '{role_name}' n'existe pas. Exécutez d'abord 'python manage.py init_roles'."
                    )
                )
                continue

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={"email": data["email"], "is_staff": True},
            )

            if created:
                user.set_password(data["password"])
                user.save()
                status_txt = "Créé"
            else:
                status_txt = "Existant"

            user.groups.add(group)
            
            # Compte le nombre de permissions héritées
            perms_count = group.permissions.count()

            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✅ [{status_txt}] Utilisateur '{user.username}' -> Rôle '{role_name}' ({perms_count} permissions)."
                )
            )

        self.stdout.write(self.style.SUCCESS("\n✅ Phase de peuplement terminée !"))