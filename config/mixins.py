"""
Mixins partagés pour l'isolation multi-agence.

Ce module fournit des classes utilitaires permettant de récupérer
l'agence de l'utilisateur connecté à partir de son compte employé.
"""

from rh.infrastructure.models import Employe


class AgenceMixin:
    """
    Mixin fournissant des méthodes utilitaires pour déterminer
    l'agence de l'utilisateur connecté.

    Méthodes :
        get_agence_id() -> UUID | None
            Retourne l'identifiant de l'agence de l'employé lié.
    """

    def get_agence_id(self):
        """
        Retourne l'identifiant de l'agence de l'utilisateur connecté.

        Returns:
            UUID | None: L'identifiant de l'agence, ou None si aucun employé
            n'est associé à l'utilisateur ou si l'employé n'a pas d'agence.
        """
        user = self.request.user
        if not user.is_authenticated:
            return None

        try:
            # Utilise la relation OneToOne définie dans Employe
            employe = user.employe_rh
            return employe.agence_id
        except Employe.DoesNotExist:
            return None