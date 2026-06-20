"""
ViewSet pour l'API des pièces détachées.
Expose les endpoints REST : GET, POST, GET detail, PUT, PATCH, DELETE.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
from decimal import Decimal

from maintenance.infrastructure.repositories.django_piece_repository import DjangoPieceDetacheeRepository
from maintenance.presentation.serializers.piece_serializer import PieceDetacheeSerializer
from maintenance.domain.entities.piece_detachee import PieceDetachee


class PieceDetacheeViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer les pièces détachées.
    Permet : lister, créer, lire, modifier et supprimer des pièces.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoPieceDetacheeRepository()

    def list(self, request):
        """GET /pieces/ -> liste toutes les pièces détachées."""
        pieces = self.repo.find_all()
        serializer = PieceDetacheeSerializer(pieces, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST /pieces/ -> crée une nouvelle pièce détachée.
        Attend un JSON avec les champs : reference, nom, prix_unitaire, stock.
        """
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
            stock=data['stock']
        )
        self.repo.add(piece)

        output = PieceDetacheeSerializer(piece).data
        return Response(output, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """GET /pieces/{id}/ -> détail d'une pièce."""
        piece = self.repo.get(UUID(pk))
        if not piece:
            return Response({"error": "Pièce non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PieceDetacheeSerializer(piece)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        PUT /pieces/{id}/ -> remplacement complet d'une pièce.
        """
        piece = self.repo.get(UUID(pk))
        if not piece:
            return Response({"error": "Pièce non trouvée"}, status=status.HTTP_404_NOT_FOUND)

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
        """
        PATCH /pieces/{id}/ -> mise à jour partielle.
        Seuls les champs fournis sont modifiés.
        """
        piece = self.repo.get(UUID(pk))
        if not piece:
            return Response({"error": "Pièce non trouvée"}, status=status.HTTP_404_NOT_FOUND)

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
        """
        DELETE /pieces/{id}/ -> supprime définitivement une pièce.
        """
        piece = self.repo.get(UUID(pk))
        if not piece:
            return Response({"error": "Pièce non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        self.repo.remove(piece)
        return Response(status=status.HTTP_204_NO_CONTENT)