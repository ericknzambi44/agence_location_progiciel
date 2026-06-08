from rest_framework import serializers
from datetime import datetime
from uuid import UUID

class PlanifierInterventionInputDTO(serializers.Serializer):
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField()
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    description_panne = serializers.CharField(required=False, allow_blank=True)

class InterventionOutputDTO(serializers.Serializer):
    id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField(allow_null=True)
    statut = serializers.CharField()
    date_debut_prevue = serializers.DateTimeField()
    date_fin_prevue = serializers.DateTimeField()
    date_debut_reelle = serializers.DateTimeField(allow_null=True)
    date_fin_reelle = serializers.DateTimeField(allow_null=True)
    description_panne = serializers.CharField()
    rapport_final = serializers.CharField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)

    @staticmethod
    def from_entity(intervention):
        return InterventionOutputDTO({
            'id': intervention.id,
            'bien_id': intervention.bien.id,
            'technicien_id': intervention.technicien.id if intervention.technicien else None,
            'statut': intervention.statut.value,
            'date_debut_prevue': intervention.date_debut_prevue,
            'date_fin_prevue': intervention.date_fin_prevue,
            'date_debut_reelle': intervention.date_debut_reelle,
            'date_fin_reelle': intervention.date_fin_reelle,
            'description_panne': intervention.description_panne,
            'rapport_final': intervention.rapport_final,
            'cout_total': intervention.cout_total.montant if intervention.cout_total else None
        }).data