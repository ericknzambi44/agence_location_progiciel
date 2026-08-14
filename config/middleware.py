"""
Middleware d'audit et d'isolation multi-agence.

(Exemple simplifié : ce middleware peut être utilisé pour charger
l'employé lié et son agence dans chaque requête.)
"""

from rh.infrastructure.models import Employe


class EmployeeMiddleware:
    """
    Middleware qui attache l'employé lié à l'utilisateur connecté
    dans la requête (request.employee).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                employe = Employe.objects.get(email=user.email)
                request.employee = employe
            except Employe.DoesNotExist:
                request.employee = None
        else:
            request.employee = None
        response = self.get_response(request)
        return response