"""
Mixin pour les ViewSets qui doivent filtrer par agence.
"""
from rest_framework.exceptions import PermissionDenied
from rh.infrastructure.models import EmployeModel


class AgenceMixin:
    """
    Fournit la méthode get_agence_id() pour récupérer l'agence de l'utilisateur.
    """

    def get_agence_id(self):
        """
        Retourne l'ID de l'agence de l'utilisateur connecté.
        - Si l'utilisateur est superuser, retourne None (pas de filtre).
        - Sinon, recherche l'employé via son email.
        - Lève PermissionDenied si l'utilisateur n'a pas d'agence.
        """
        user = self.request.user

        # Les superusers voient toutes les données (pas de filtre)
        if user.is_superuser:
            return None

        # Récupérer l'employé à partir de l'email
        try:
            employe = EmployeModel.objects.get(email=user.email)
        except EmployeModel.DoesNotExist:
            raise PermissionDenied(
                "Aucun employé associé à cet utilisateur. Veuillez contacter l'administrateur."
            )

        if not employe.agence_id:
            raise PermissionDenied(
                "Cet utilisateur n'est pas rattaché à une agence. Veuillez contacter l'administrateur."
            )

        return employe.agence_id