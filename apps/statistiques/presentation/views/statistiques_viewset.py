from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from datetime import date
from statistiques.application.services.agregation_service import AggregationService
from statistiques.infrastructure.repositories.django_statistiques_repository import DjangoStatistiquesRepository
from statistiques.presentation.serializers.statistiques_serializers import (
    PeriodeInputSerializer,
    RevenuParPeriodeSerializer,
    RevenuParBienSerializer,
    RevenuParClientSerializer,
    ContratParPeriodeSerializer,
    ContratParStatutSerializer,
    BienPopulaireSerializer,
    PiecePopulaireSerializer,
    InterventionTechnicienSerializer,
    StatistiquesInterventionsSerializer,
    ClientActifSerializer,
    SyntheseSerializer,
)
from statistiques.domain.value_objects.periode import UnitePeriode

class StatistiquesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoStatistiquesRepository()
        self.service = AggregationService(self.repo)

    def _get_periode(self, request):
        serializer = PeriodeInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['debut'], serializer.validated_data['fin']

    @action(detail=False, methods=['get'], url_path='revenus')
    def revenus(self, request):
        debut, fin = self._get_periode(request)
        unite = request.query_params.get('unite', 'mois')
        unite_map = {'jour': UnitePeriode.JOUR, 'mois': UnitePeriode.MOIS, 'annee': UnitePeriode.ANNEE}
        unite = unite_map.get(unite, UnitePeriode.MOIS)
        data = self.service.get_revenus(debut, fin, unite)
        serializer = RevenuParPeriodeSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='revenus-par-bien')
    def revenus_par_bien(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_revenus_par_bien(debut, fin)
        serializer = RevenuParBienSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='revenus-par-client')
    def revenus_par_client(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_revenus_par_client(debut, fin)
        serializer = RevenuParClientSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='contrats')
    def contrats(self, request):
        debut, fin = self._get_periode(request)
        unite = request.query_params.get('unite', 'mois')
        unite_map = {'jour': UnitePeriode.JOUR, 'mois': UnitePeriode.MOIS, 'annee': UnitePeriode.ANNEE}
        unite = unite_map.get(unite, UnitePeriode.MOIS)
        data = self.service.get_contrats_par_periode(debut, fin, unite)
        serializer = ContratParPeriodeSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='contrats-statut')
    def contrats_statut(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_contrats_par_statut(debut, fin)
        serializer = ContratParStatutSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='taux-occupation')
    def taux_occupation(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_taux_occupation_global(debut, fin)
        return Response({"taux": data})

    @action(detail=False, methods=['get'], url_path='biens-populaires')
    def biens_populaires(self, request):
        debut, fin = self._get_periode(request)
        limite = int(request.query_params.get('limite', 5))
        data = self.service.get_biens_populaires(debut, fin, limite)
        serializer = BienPopulaireSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pieces-populaires')
    def pieces_populaires(self, request):
        debut, fin = self._get_periode(request)
        limite = int(request.query_params.get('limite', 5))
        data = self.service.get_pieces_populaires(debut, fin, limite)
        serializer = PiecePopulaireSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='interventions-techniciens')
    def interventions_techniciens(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_interventions_techniciens(debut, fin)
        serializer = InterventionTechnicienSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='statistiques-interventions')
    def statistiques_interventions(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_statistiques_interventions(debut, fin)
        serializer = StatistiquesInterventionsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='clients-actifs')
    def clients_actifs(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_clients_actifs(debut, fin)
        return Response({"nb_clients_actifs": data})

    @action(detail=False, methods=['get'], url_path='clients-plus-actifs')
    def clients_plus_actifs(self, request):
        debut, fin = self._get_periode(request)
        limite = int(request.query_params.get('limite', 5))
        data = self.service.get_clients_plus_actifs(debut, fin, limite)
        serializer = ClientActifSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='synthese')
    def synthese(self, request):
        debut, fin = self._get_periode(request)
        data = self.service.get_synthese(debut, fin)
        serializer = SyntheseSerializer(data)
        return Response(serializer.data)