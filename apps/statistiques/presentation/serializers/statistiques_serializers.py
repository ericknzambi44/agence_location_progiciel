from rest_framework import serializers
from datetime import date

class PeriodeInputSerializer(serializers.Serializer):
    debut = serializers.DateField()
    fin = serializers.DateField()

class RevenuParPeriodeSerializer(serializers.Serializer):
    periode_label = serializers.DateField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)

class RevenuParBienSerializer(serializers.Serializer):
    bien_id = serializers.UUIDField()
    nom = serializers.CharField()
    total_revenus = serializers.DecimalField(max_digits=12, decimal_places=2)
    nb_contrats = serializers.IntegerField()

class RevenuParClientSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
    total_depense = serializers.DecimalField(max_digits=12, decimal_places=2)
    nb_contrats = serializers.IntegerField()

class ContratParPeriodeSerializer(serializers.Serializer):
    periode_label = serializers.DateField()
    total = serializers.IntegerField()

class ContratParStatutSerializer(serializers.Serializer):
    actif = serializers.IntegerField()
    termine = serializers.IntegerField()
    annule = serializers.IntegerField()

class BienPopulaireSerializer(serializers.Serializer):
    bien_id = serializers.UUIDField()
    nom = serializers.CharField()
    reference = serializers.CharField()
    nb_contrats = serializers.IntegerField()
    revenus = serializers.DecimalField(max_digits=12, decimal_places=2)

class PiecePopulaireSerializer(serializers.Serializer):
    piece_id = serializers.UUIDField()
    nom = serializers.CharField()
    reference = serializers.CharField()
    quantite_totale = serializers.IntegerField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2)

class InterventionTechnicienSerializer(serializers.Serializer):
    technicien_id = serializers.UUIDField(required=False, allow_null=True)
    nom = serializers.CharField()
    nb_interventions = serializers.IntegerField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    duree_moyenne = serializers.FloatField()

class StatistiquesInterventionsSerializer(serializers.Serializer):
    nb_total = serializers.IntegerField()
    cout_moyen = serializers.DecimalField(max_digits=12, decimal_places=2)
    duree_moyenne_heures = serializers.FloatField()
    duree_min_heures = serializers.FloatField()
    duree_max_heures = serializers.FloatField()
    ecart_type_heures = serializers.FloatField()

class ClientActifSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
    nb_contrats = serializers.IntegerField()
    total_depense = serializers.DecimalField(max_digits=12, decimal_places=2)

class SyntheseSerializer(serializers.Serializer):
    revenus = RevenuParPeriodeSerializer(many=True)
    contrats = ContratParPeriodeSerializer(many=True)
    contrats_statut = ContratParStatutSerializer()
    taux_occupation = serializers.FloatField()
    biens_populaires = BienPopulaireSerializer(many=True)
    pieces_populaires = PiecePopulaireSerializer(many=True)
    interventions_techniciens = InterventionTechnicienSerializer(many=True)
    clients_actifs = serializers.IntegerField()
    statistiques_interventions = StatistiquesInterventionsSerializer()