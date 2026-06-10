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
    technicien_id = serializers.UUIDField(source='technicien.id', read_only=True)
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    statut = serializers.CharField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2, source='_cout_total')

    @staticmethod
    def from_entity(intervention):
     return {
        'id': str(intervention.id),
        'bien_id': str(intervention.bien_id),
        'technicien_id': str(intervention.technicien.id) if intervention.technicien else None,
        'date_debut': intervention.date_debut.isoformat() if intervention.date_debut else None,
        'date_fin': intervention.date_fin.isoformat() if intervention.date_fin else None,
        'statut': intervention.statut,
        'cout_total': float(intervention._cout_total) if hasattr(intervention, '_cout_total') else 0.0,
    }

class AjoutPieceSerializer(serializers.Serializer):
    piece_id = serializers.UUIDField()
    quantite = serializers.IntegerField(min_value=1)