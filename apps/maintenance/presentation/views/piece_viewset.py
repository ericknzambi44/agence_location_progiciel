"""
Module de Présentation - Pièces Détachées (Clean Architecture / DDD)

Expose la gestion du stock de pièces détachées destinées à la maintenance.
Sécurité assurée par le RBAC (HasModulePermission) et l'isolation multi-agence (AgenceMixin).
"""

from decimal import Decimal
from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.permissions import HasModulePermission
from config.mixins import AgenceMixin
from maintenance.domain.entities.piece_detachee import PieceDetachee
from maintenance.infrastructure.repositories.django_piece_repository import (
    DjangoPieceDetacheeRepository,
)
from maintenance.presentation.serializers.piece_serializer import PieceDetacheeSerializer


class PieceDetacheeViewSet(AgenceMixin, viewsets.ViewSet):
    """
    ViewSet gérant le CRUD du catalogue des pièces détachées par agence.

    Attributs DDD / RBAC :
        permission_classes: Validation RBAC sur le module Maintenance.
        required_module: Module applicatif ciblé ('maintenance').
        required_model: Modèle de domaine ciblé ('piecedetacheemodel').
    """

    permission_classes = [HasModulePermission]
    required_module = 'maintenance'
    required_model = 'piecedetacheemodel'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Injection du repository de pièces détachées
        self.repo = DjangoPieceDetacheeRepository()

    def list(self, request):
        """
        Consulte le stock des pièces détachées de l'agence.

        Permission requise : maintenance.view_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        pieces = self.repo.find_all(agence_id=agence_id)
        serializer = PieceDetacheeSerializer(pieces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Consulte les détails d'une pièce détachée spécifique.

        Permission requise : maintenance.view_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        try:
            piece_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID de pièce invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        piece = self.repo.get(piece_uuid, agence_id=agence_id)
        if not piece:
            return Response(
                {"error": "Pièce détachée non trouvée ou non autorisée pour votre agence."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PieceDetacheeSerializer(piece)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre une nouvelle référence de pièce détachée dans l'agence.

        Permission requise : maintenance.add_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        serializer = PieceDetacheeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        piece = PieceDetachee(
            reference=data['reference'],
            nom=data['nom'],
            prix_unitaire=Decimal(str(data['prix_unitaire'])),
            stock=data['stock'],
            agence_id=agence_id,
        )
        self.repo.add(piece)

        output = PieceDetacheeSerializer(piece).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Met à jour intégralement une pièce détachée.

        Permission requise : maintenance.change_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        try:
            piece_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID de pièce invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        piece = self.repo.get(piece_uuid, agence_id=agence_id)
        if not piece:
            return Response(
                {"error": "Pièce détachée non trouvée ou non autorisée."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PieceDetacheeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        piece.reference = data['reference']
        piece.nom = data['nom']
        piece.prix_unitaire = Decimal(str(data['prix_unitaire']))
        piece.stock = data['stock']
        self.repo.update(piece)

        output = PieceDetacheeSerializer(piece).data
        return Response(output, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Mise à jour partielle des informations d'une pièce détachée.

        Permission requise : maintenance.change_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        try:
            piece_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID de pièce invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        piece = self.repo.get(piece_uuid, agence_id=agence_id)
        if not piece:
            return Response(
                {"error": "Pièce détachée non trouvée ou non autorisée."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PieceDetacheeSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"error": "Données invalides.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        return Response(output, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Supprime une pièce détachée du catalogue.

        Permission requise : maintenance.delete_piecedetacheemodel
        """
        agence_id = self.get_agence_id()

        try:
            piece_uuid = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {"error": "Identifiant UUID de pièce invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        piece = self.repo.get(piece_uuid, agence_id=agence_id)
        if not piece:
            return Response(
                {"error": "Pièce détachée non trouvée ou non autorisée."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.repo.remove(piece)
        return Response(status=status.HTTP_204_NO_CONTENT)