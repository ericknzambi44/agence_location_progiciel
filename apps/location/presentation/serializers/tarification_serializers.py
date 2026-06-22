"""
Serializers pour la gestion des règles de tarification.
"""
from rest_framework import serializers
from location.domain.value_objects.regle_tarification import TypeRegle


class TypeRegleField(serializers.Field):
    """
    Champ personnalisé pour sérialiser/désérialiser les valeurs de TypeRegle.
    """
    def to_representation(self, value):
        # Convertit l'énumération en chaîne
        if isinstance(value, TypeRegle):
            return value.value
        return value

    def to_internal_value(self, data):
        # Convertit la chaîne en énumération
        try:
            return TypeRegle(data)
        except ValueError:
            raise serializers.ValidationError(f"Type invalide : {data}. Choisir parmi {[t.value for t in TypeRegle]}")


class RegleTarificationSerializer(serializers.Serializer):
    """Serialise une règle individuelle."""
    type = TypeRegleField()  # Utilise le champ personnalisé
    valeur = serializers.DecimalField(max_digits=10, decimal_places=2)
    duree_min = serializers.IntegerField(min_value=0)
    duree_max = serializers.IntegerField(required=False, allow_null=True)
    type_bien_id = serializers.UUIDField(required=False, allow_null=True)
    periode_debut = serializers.DateField(required=False, allow_null=True)
    periode_fin = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)


class RegleTarificationInputSerializer(serializers.Serializer):
    """Serialiseur pour la requête POST /tarification/."""
    regles = RegleTarificationSerializer(many=True)


class RegleTarificationOutputSerializer(RegleTarificationSerializer):
    """Serialiseur pour la réponse GET /tarification/."""
    pass