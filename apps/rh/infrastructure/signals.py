"""
Signaux pour le module RH.

Synchronise les groupes entre l'employé et l'utilisateur Django associé.
"""

from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rh.infrastructure.models import Employe


@receiver(m2m_changed, sender=Employe.groups.through)
def sync_user_groups_from_employe(sender, instance, action, reverse, pk_set, **kwargs):
    """
    Quand les groupes de l'Employe changent (ajout, suppression, réinitialisation),
    met à jour les groupes de l'utilisateur lié.
    """
    # On ne traite que si l'instance est un Employe (et non un Group, dans le cas reverse)
    if isinstance(instance, Employe):
        if action in ['post_add', 'post_remove', 'post_clear']:
            if instance.user:
                # Synchronise les groupes de l'utilisateur avec ceux de l'employé
                instance.user.groups.set(instance.groups.all())