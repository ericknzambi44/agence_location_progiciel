"""
Sérialiseurs pour la gestion des règles de tarification de maintenance.
"""

from rest_framework import serializers
from maintenance.domain.value_objects.regle_maintenance import TypeRegleMaintenance


class TypeRegleMaintenanceField(serializers.Field):
    """
    Champ personnalisé pour sérialiser/désérialiser les valeurs de TypeRegleMaintenance.
    """

    def to_representation(self, value):
        if isinstance(value, TypeRegleMaintenance):
            return value.value
        return value

    def to_internal_value(self, data):
        try:
            return TypeRegleMaintenance(data)
        except ValueError:
            raise serializers.ValidationError(
                f"Type invalide : {data}. Choisir parmi {[t.value for t in TypeRegleMaintenance]}"
            )


class RegleMaintenanceSerializer(serializers.Serializer):
    """
    Serializer pour une règle de tarification de maintenance.
    """

    type = TypeRegleMaintenanceField()
    valeur = serializers.DecimalField(max_digits=10, decimal_places=2)
    duree_min = serializers.IntegerField(min_value=0, default=0)
    duree_max = serializers.IntegerField(required=False, allow_null=True)
    periode_debut = serializers.DateField(required=False, allow_null=True)
    periode_fin = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)


class RegleMaintenanceInputSerializer(serializers.Serializer):
    """
    Serializer pour la requête POST /regles-maintenance/.
    """

    regles = RegleMaintenanceSerializer(many=True)


class RegleMaintenanceOutputSerializer(RegleMaintenanceSerializer):
    """
    Serializer pour la réponse GET /regles-maintenance/.
    """

    pass