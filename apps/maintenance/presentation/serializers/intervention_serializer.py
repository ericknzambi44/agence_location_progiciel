from rest_framework import serializers

class InterventionInputSerializer(serializers.Serializer):
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField()
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    description_panne = serializers.CharField(required=False, allow_blank=True, default="")

class InterventionOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField()
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    statut = serializers.CharField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2)

    @staticmethod
    def from_entity(intervention):
        return {
            'id': str(intervention.id),
            'bien_id': str(intervention.bien_id),
            'technicien_id': str(intervention.technicien.id),
            'date_debut': intervention.date_debut.isoformat(),
            'date_fin': intervention.date_fin.isoformat(),
            'statut': intervention.statut.value,
            'cout_total': float(intervention.cout_total),
        }

class AjoutPieceSerializer(serializers.Serializer):
    piece_id = serializers.UUIDField()
    quantite = serializers.IntegerField(min_value=1)