"""
Sérialiseurs REST pour l'entité Bien.

Ces sérialiseurs sont volontairement déclaratifs et indépendants
du modèle Django (approche Clean Architecture). Ils manipulent
l'entité domaine `Bien` et son Value Object `PrixHT`.

On utilise `source` pour extraire les attributs des Value Objects :
    - prix_unitaire_ht.amount   -> montant
    - prix_unitaire_ht.currency -> devise
    - etat.value                -> valeur de l'enum EtatBien
"""

from rest_framework import serializers


class BienInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour la création ou la mise à jour d'un bien.

    Champs attendus :
        - reference (str)         : référence unique du bien
        - nom (str)               : nom du bien
        - description (str)       : description optionnelle
        - prix_unitaire_ht (float): prix unitaire hors taxe
        - devise (str)            : code devise (ex: USD, CDF)
        - date_achat (date)       : date d'achat optionnelle
    """

    reference = serializers.CharField(max_length=50)
    nom = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    prix_unitaire_ht = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    devise = serializers.CharField(max_length=3, default='USD', required=False)
    date_achat = serializers.DateField(required=False, allow_null=True)


class BienOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie représentant un bien.
    Mappe directement les attributs de l'entité domaine `Bien`.
    """

    id = serializers.UUIDField()
    reference = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField(required=False)
    prix_unitaire_ht = serializers.DecimalField(
        source='prix_unitaire_ht.amount',
        max_digits=12,
        decimal_places=2
    )
    devise = serializers.CharField(
        source='prix_unitaire_ht.currency',
        max_length=3
    )
    date_achat = serializers.DateField(required=False, allow_null=True)
    etat = serializers.CharField(source='etat.value')