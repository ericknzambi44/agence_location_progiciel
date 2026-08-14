# create_permissions.py
"""
Script de création/synchronisation des permissions pour les modules RH, Stock, Maintenance, etc.
À exécuter avec : python manage.py shell < create_permissions.py
"""

# create_permissions.py 
from django.apps import apps
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

APP_LABELS = ['rh', 'stock', 'maintenance', 'administration', 'location', 'authentication']

def create_permissions_for_app(app_label):
    try:
        app_config = apps.get_app_config(app_label)
    except LookupError:
        print(f"❌ Application '{app_label}' introuvable.")
        return
    for model in app_config.get_models():
        content_type = ContentType.objects.get_for_model(model)
        for action in ['add', 'change', 'delete', 'view']:
            codename = f"{action}_{model._meta.model_name}"
            name = f"Can {action} {model._meta.verbose_name}"
            Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={'name': name}
            )
    print(f"--- Permissions vérifiées pour '{app_label}' ---")

for app_label in APP_LABELS:
    create_permissions_for_app(app_label)

# Mapping des groupes avec les vrais noms des modèles (avec suffixe "Model" si nécessaire)
group_mapping = {
    "Chef d'Agence RH": {
        'rh': ['employe', 'pointage', 'evaluation', 'role'],
        'stock': ['bienmodel', 'categoriemodel'],
    },
    "Gestionnaire Stock": {
        'stock': ['bienmodel', 'categoriemodel', 'mouvementstockmodel', 'disponibiliteperiodemodel'],
    },
    "Technicien Maintenance": {
        'maintenance': ['technicienmodel', 'piecedetacheemodel', 'interventionmodel', 'interventionpiecemodel', 'reglemaintenancemodel'],
        'stock': ['bienmodel'],
    },
}

for group_name, modules in group_mapping.items():
    group, _ = Group.objects.get_or_create(name=group_name)
    group.permissions.clear()
    assigned = 0
    for app_label, model_names in modules.items():
        try:
            app_config = apps.get_app_config(app_label)
            for model_name in model_names:
                # Cherche le modèle exact par model_name
                model = app_config.get_model(model_name)
                perms = Permission.objects.filter(
                    content_type__app_label=app_label,
                    content_type__model=model._meta.model_name
                )
                group.permissions.add(*perms)
                assigned += perms.count()
        except Exception as e:
            print(f"⚠️ Erreur avec '{app_label}.{model_name}': {e}")
    print(f"✅ Groupe '{group_name}' : {group.permissions.count()} permissions assignées.")

# SuperAdmin
super_group, _ = Group.objects.get_or_create(name="SuperAdmin")
super_group.permissions.set(Permission.objects.all())
print(f"✅ Groupe 'SuperAdmin' : {super_group.permissions.count()} permissions assignées.")


#commande: python manage.py shell < create_permissions.py