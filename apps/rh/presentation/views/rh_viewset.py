from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from uuid import UUID
from datetime import date

from rh.application.consulter_pointages import ConsulterPointagesUseCase
from rh.application.embaucher_employe import EmbaucherEmployeUseCase
from rh.application.enregistrer_pointage import EnregistrerPointageUseCase
from rh.presentation.serializers.rh_serializers import (
    EmployeInputSerializer, EmployeOutputSerializer,
    PointageInputSerializer, PointageOutputSerializer,
)

from rh.infrastructure.repositories.django_employe_repository import DjangoEmployeRepository
from rh.infrastructure.repositories.django_pointage_repository import DjangoPointageRepository

class RHViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employe_repo = DjangoEmployeRepository()
        self.pointage_repo = DjangoPointageRepository()

    # Méthode list ajoutée
    def list(self, request):
        employes = self.employe_repo.list_actifs()
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data)

    # Méthode create pour embaucher
    def create(self, request):
        serializer = EmployeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uc = EmbaucherEmployeUseCase(self.employe_repo)
        try:
            employe = uc.execute(
                matricule_str=data['matricule'],
                nom=data['nom'],
                prenom=data['prenom'],
                email_str=data['email'],
                date_embauche=data['date_embauche'],
                taux_valeur=data['taux_horaire'],
                poste=data['poste']
            )
            output = EmployeOutputSerializer(employe).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='actifs')
    def lister_actifs(self, request):
        employes = self.employe_repo.list_actifs()
        serializer = EmployeOutputSerializer(employes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='pointages')
    def enregistrer_pointage(self, request):
        serializer = PointageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uc = EnregistrerPointageUseCase(self.employe_repo, self.pointage_repo)
        try:
            pointage = uc.execute(
                employe_id=data['employe_id'],
                type_str=data['type'],
                horodatage=data.get('horodatage')
            )
            output = PointageOutputSerializer(pointage).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='pointages/(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})')
    def consulter_pointages(self, request, pk=None, date_str=None):
        try:
            jour = date.fromisoformat(date_str)
        except ValueError:
            return Response({"error": "Format de date invalide (YYYY-MM-DD)"}, status=400)
        uc = ConsulterPointagesUseCase(self.pointage_repo, self.employe_repo)
        try:
            pointages = uc.execute(UUID(pk), jour)
            serializer = PointageOutputSerializer(pointages, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)