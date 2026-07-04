"""
ViewSet pour la gestion des techniciens (maintenance).
Toutes les opérations sont filtrées par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from decimal import Decimal

from config.mixins import AgenceMixin

from maintenance.infrastructure.repositories.django_technicien_repository import DjangoTechnicienRepository
from maintenance.presentation.serializers.technicien_serializer import TechnicienSerializer
from maintenance.domain.entities.technicien import Technicien
from shared_kernel.domain.value_objects import Email, PersonName


class TechnicienViewSet(AgenceMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoTechnicienRepository()

    def list(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        techniciens = self.repo.get_all(agence_id=agence_id)
        serializer = TechnicienSerializer(techniciens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = TechnicienSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            technicien = Technicien(
                nom=PersonName(data['nom']),
                prenom=PersonName(data['prenom']),
                email=Email(data['email']),
                cout_horaire=Decimal(str(data['cout_horaire'])),
                agence_id=agence_id
            )
            self.repo.add(technicien)
            output = TechnicienSerializer(technicien).data
            return Response(output, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)