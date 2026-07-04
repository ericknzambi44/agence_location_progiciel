"""
ViewSet pour l'API des pièces détachées.
Toutes les opérations sont filtrées par agence via AgenceMixin.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from uuid import UUID
from decimal import Decimal

from config.mixins import AgenceMixin

from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository
from maintenance.presentation.serializers.piece_serializer import PieceDetacheeSerializer
from maintenance.domain.entities.piece_detachee import PieceDetachee


class PieceDetacheeViewSet(AgenceMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoPieceDetacheeRepository()

    def list(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        pieces = self.repo.find_all(agence_id=agence_id)
        serializer = PieceDetacheeSerializer(pieces, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = PieceDetacheeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        piece = PieceDetachee(
            reference=data['reference'],
            nom=data['nom'],
            prix_unitaire=Decimal(str(data['prix_unitaire'])),
            stock=data['stock'],
            agence_id=agence_id
        )
        self.repo.add(piece)

        output = PieceDetacheeSerializer(piece).data
        return Response(output, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        piece = self.repo.get(UUID(pk), agence_id=agence_id)
        if not piece:
            return Response({"error": "Pièce non trouvée ou non autorisée"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PieceDetacheeSerializer(piece)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        piece = self.repo.get(UUID(pk), agence_id=agence_id)
        if not piece:
            return Response({"error": "Pièce non trouvée ou non autorisée"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PieceDetacheeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        piece.reference = data['reference']
        piece.nom = data['nom']
        piece.prix_unitaire = Decimal(str(data['prix_unitaire']))
        piece.stock = data['stock']
        self.repo.update(piece)

        output = PieceDetacheeSerializer(piece).data
        return Response(output)

    def partial_update(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        piece = self.repo.get(UUID(pk), agence_id=agence_id)
        if not piece:
            return Response({"error": "Pièce non trouvée ou non autorisée"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PieceDetacheeSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        if 'reference' in data:
            piece.reference = data['reference']
        if 'nom' in data:
            piece.nom = data['nom']
        if 'prix_unitaire' in data:
            piece.prix_unitaire = Decimal(str(data['prix_unitaire']))
        if 'stock' in data:
            piece.stock = data['stock']

        self.repo.update(piece)
        output = PieceDetacheeSerializer(piece).data
        return Response(output)

    def destroy(self, request, pk=None):
        try:
            agence_id = self.get_agence_id()
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        piece = self.repo.get(UUID(pk), agence_id=agence_id)
        if not piece:
            return Response({"error": "Pièce non trouvée ou non autorisée"}, status=status.HTTP_404_NOT_FOUND)
        self.repo.remove(piece)
        return Response(status=status.HTTP_204_NO_CONTENT)