"""
Serializers pour la gestion des règles de tarification.
Supportent les nouveaux champs bien_id et categorie_id.
"""
from rest_framework import serializers
from location.domain.value_objects.regle_tarification import TypeRegle


class TypeRegleField(serializers.Field):
    """
    Champ personnalisé pour sérialiser/désérialiser les valeurs de TypeRegle.
    Convertit l'énumération en chaîne et vice-versa.
    """
    def to_representation(self, value):
        if isinstance(value, TypeRegle):
            return value.value
        return value

    def to_internal_value(self, data):
        try:
            return TypeRegle(data)
        except ValueError:
            raise serializers.ValidationError(
                f"Type invalide : {data}. Choisir parmi {[t.value for t in TypeRegle]}"
            )


class RegleTarificationSerializer(serializers.Serializer):
    """
    Serializer pour une règle de tarification individuelle.
    Remplace type_bien_id par bien_id et ajoute categorie_id.
    """
    type = TypeRegleField()
    valeur = serializers.DecimalField(max_digits=10, decimal_places=2)
    duree_min = serializers.IntegerField(min_value=0)
    duree_max = serializers.IntegerField(required=False, allow_null=True)

    #ciblage par bien ou par catégorie
    bien_id = serializers.UUIDField(required=False, allow_null=True)
    categorie_id = serializers.UUIDField(required=False, allow_null=True)

    periode_debut = serializers.DateField(required=False, allow_null=True)
    periode_fin = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)

    def validate(self, data):
        """
        Validation métier : une règle ne peut pas cibler à la fois un bien et une catégorie.
        """
        bien_id = data.get('bien_id')
        categorie_id = data.get('categorie_id')
        if bien_id is not None and categorie_id is not None:
            raise serializers.ValidationError(
                "Une règle ne peut pas cibler à la fois un bien spécifique et une catégorie."
            )
        return data


class RegleTarificationInputSerializer(serializers.Serializer):
    """
    Serializer pour la requête POST /tarification/.
    Attend une liste de règles.
    """
    regles = RegleTarificationSerializer(many=True)


class RegleTarificationOutputSerializer(RegleTarificationSerializer):
    """
    Serializer pour la réponse GET /tarification/.
    Hérite de RegleTarificationSerializer.
    """
    pass