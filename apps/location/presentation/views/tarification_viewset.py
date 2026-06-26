"""
ViewSet pour la gestion des règles de tarification.
Expose les endpoints GET et POST /api/location/tarification/.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID

from location.application.services.tarification_service import TarificationService
from location.application.use_cases.configurer_tarification import ConfigurerTarificationUseCase
from location.application.use_cases.consulter_regles import ConsulterReglesUseCase
from location.infrastructure.repositories.django_regle_tarification_repository import (
    DjangoRegleTarificationRepository
)
from administration.infrastructure.repositories.django_agence_repository import DjangoAgenceRepository
from location.presentation.serializers.tarification_serializers import (
    RegleTarificationInputSerializer,
    RegleTarificationOutputSerializer
)
from location.domain.value_objects.regle_tarification import RegleTarification, TypeRegle
from location.domain.entities.regle_tarification import ReglesTarification


class TarificationViewSet(viewsets.ViewSet):
    """
    ViewSet pour la tarification dynamique.
    - GET /tarification/  → liste les règles actuelles
    - POST /tarification/ → enregistre de nouvelles règles
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRegleTarificationRepository()
        self.service = TarificationService(self.repo)

    def list(self, request):
        """
        Récupère les règles de tarification pour l'agence par défaut.
        """
        agence_repo = DjangoAgenceRepository()
        agences = agence_repo.list_actives()
        if not agences:
            return Response({"error": "Aucune agence active trouvée."}, status=status.HTTP_404_NOT_FOUND)

        agence_id = agences[0].id
        regles = self.service.get_regles(agence_id)
        serializer = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Enregistre les règles de tarification pour l'agence par défaut.
        Remplace les règles existantes par les nouvelles.
        """
        agence_repo = DjangoAgenceRepository()
        agences = agence_repo.list_actives()
        if not agences:
            return Response({"error": "Aucune agence active trouvée."}, status=status.HTTP_404_NOT_FOUND)

        agence_id = agences[0].id

        # Validation des données d'entrée
        serializer = RegleTarificationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        regles_data = serializer.validated_data['regles']

        # Construction des objets du domaine 
        regles_obj = []
        for r in regles_data:
            regle = RegleTarification(
                type=TypeRegle(r['type']),
                valeur=r['valeur'],
                duree_min=r['duree_min'],
                duree_max=r.get('duree_max'),
                bien_id=r.get('bien_id'),         
                categorie_id=r.get('categorie_id'),  
                periode_debut=r.get('periode_debut'),
                periode_fin=r.get('periode_fin'),
                description=r.get('description', ''),
                active=r.get('active', True)
            )
            regles_obj.append(regle)

        # Créer l'agrégat
        regles_aggregat = ReglesTarification(agence_id=agence_id, regles=regles_obj)

        # Exécuter le use case
        uc = ConfigurerTarificationUseCase(self.repo)
        uc.execute(agence_id, regles_aggregat)

        # Retourner la liste mise à jour
        regles = self.service.get_regles(agence_id)
        output = RegleTarificationOutputSerializer(regles.regles, many=True)
        return Response(output.data, status=status.HTTP_200_OK)