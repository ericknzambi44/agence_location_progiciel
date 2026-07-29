"""
Module de Présentation - Ressources Humaines (Clean Architecture / DDD)

Expose les fonctions d'embauche, de gestion des employés et de suivi des pointages.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from datetime import date
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from rh.application.consulter_pointages import ConsulterPointagesUseCase
from rh.application.embaucher_employe import EmbaucherEmployeUseCase
from rh.application.enregistrer_pointage import EnregistrerPointageUseCase
from rh.infrastructure.repositories.django_employe_repository import DjangoEmployeRepository
from rh.infrastructure.repositories.django_pointage_repository import DjangoPointageRepository
from rh.presentation.serializers.rh_serializers import (
    EmployeInputSerializer,
    EmployeOutputSerializer,
    PointageInputSerializer,
    PointageOutputSerializer,
)


class RHViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant l'administration des employés et le suivi des heures de présence (pointages).

    Attributs DDD / RBAC :
        permission_classes: Validation RBAC sur le module RH.
        required_module: Module applicatif ciblé ('rh').
    """

    permission_classes = [HasModulePermission]
    required_module = 'rh'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection des repositories d'infrastructure
        self.employe_repo = DjangoEmployeRepository()
        self.pointage_repo = DjangoPointageRepository()

    # --- GESTION DES EMPLOYÉS ---

    def list(self, request):
        """
        Consulte la liste complète des employés de l'agence.

        Permission requise : rh.view_employemodel
        """
        self.required_model = 'employemodel'
        agence_id = self.get_agence_id()

        employes = self.employe_repo.list_actifs(agence_id=agence_id)
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre l'embauche d'un nouvel employé au sein de l'agence.

        Permission requise : rh.add_employemodel
        """
        self.required_model = 'employemodel'
        agence_id = self.get_agence_id()

        serializer = EmployeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        use_case = EmbaucherEmployeUseCase(self.employe_repo)
        try:
            employe = use_case.execute(
                matricule_str=data['matricule'],
                nom=data['nom'],
                prenom=data['prenom'],
                email_str=data['email'],
                date_embauche=data['date_embauche'],
                taux_valeur=data['taux_horaire'],
                poste=data['poste'],
                agence_id=agence_id,
            )
            output = EmployeOutputSerializer(employe).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='actifs')
    def lister_actifs(self, request):
        """
        Liste les employés actuellement actifs de l'agence.

        Permission requise : rh.view_employemodel
        """
        self.required_model = 'employemodel'
        agence_id = self.get_agence_id()

        employes = self.employe_repo.list_actifs(agence_id=agence_id)
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- GESTION DES POINTAGES ---

    @action(detail=False, methods=['post'], url_path='pointages')
    def enregistrer_pointage(self, request):
        """
        Enregistre un événement de pointage (entrée/sortie) pour un employé.

        Permission requise : rh.add_pointagemodel
        """
        self.required_model = 'pointagemodel'
        agence_id = self.get_agence_id()

        serializer = PointageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Vérification de l'appartenance à l'agence
        employe = self.employe_repo.get(data['employe_id'], agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        use_case = EnregistrerPointageUseCase(self.employe_repo, self.pointage_repo)
        try:
            pointage = use_case.execute(
                employe_id=data['employe_id'],
                type_str=data['type'],
                horodatage=data.get('horodatage'),
            )
            output = PointageOutputSerializer(pointage).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='pointages/(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})')
    def consulter_pointages(self, request, pk=None, date_str=None):
        """
        Consulte l'historique des pointages d'un employé pour une journée donnée.

        Permission requise : rh.view_pointagemodel
        """
        self.required_model = 'pointagemodel'
        agence_id = self.get_agence_id()

        try:
            employe_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID d'employé invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employe = self.employe_repo.get(employe_uuid, agence_id=agence_id)
        if not employe:
            return Response(
                {"error": "Employé non trouvé ou non autorisé pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            jour = date.fromisoformat(date_str)
        except ValueError:
            return Response(
                {"error": "Format de date invalide (Format attendu : YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = ConsulterPointagesUseCase(self.pointage_repo, self.employe_repo)
        try:
            pointages = use_case.execute(employe_uuid, jour)
            serializer = PointageOutputSerializer(pointages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)