"""
Serializers pour l'API du module Stock.
Incluent la gestion de la devise pour le prix unitaire.
"""
from rest_framework import serializers


class BienInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la création ou mise à jour d'un bien.
    """
    reference = serializers.CharField(max_length=50)
    nom = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    prix_unitaire_ht = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    devise = serializers.CharField(max_length=3, default='USD', required=False)
    date_achat = serializers.DateField(required=False, allow_null=True)


class BienOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la réponse des biens.
    """
    id = serializers.UUIDField()
    reference = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField(required=False)
    prix_unitaire_ht = serializers.DecimalField(max_digits=12, decimal_places=2)
    devise = serializers.CharField(max_length=3)
    date_achat = serializers.DateField(required=False, allow_null=True)
    etat = serializers.CharField()

    @staticmethod
    def from_entity(bien):
        """
        Convertit une entité Bien en dictionnaire sérialisable.
        Extrait le montant et la devise du Value Object PrixHT.
        """
        return {
            'id': str(bien.id),
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description or '',
            'prix_unitaire_ht': bien.prix_unitaire_ht.amount,
            'devise': bien.prix_unitaire_ht.currency,
            'date_achat': bien.date_achat.isoformat() if bien.date_achat else None,
            'etat': bien.etat.value,
        }