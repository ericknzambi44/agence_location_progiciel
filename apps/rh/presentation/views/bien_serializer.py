from rest_framework import serializers
from uuid import UUID
from decimal import Decimal

class BienInputSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=50)
    nom = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    prix_unitaire_ht = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_achat = serializers.DateField(required=False, allow_null=True)

class BienOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    reference = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField(required=False)
    prix_unitaire_ht = serializers.DecimalField(max_digits=12, decimal_places=2)
    date_achat = serializers.DateField(required=False, allow_null=True)
    etat = serializers.CharField()

    @staticmethod
    def from_entity(bien):
        return BienOutputSerializer({
            'id': bien.id,
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description or '',
            'prix_unitaire_ht': bien.prix_unitaire_ht,
            'date_achat': bien.date_achat,
            'etat': bien.etat.value,
        }).data