"""
Sérialiseurs REST pour les clients et les contrats de location.

Ces sérialiseurs sont déclaratifs et indépendants des modèles Django
(approche Clean Architecture). Ils manipulent les entités domaine
`Client` et `Contrat`.

Note :
    - Le champ `montant_total` de `ContratOutputSerializer` utilise
      `source='montant_total.valeur'` car l'entité `Contrat` possède
      un Value Object `Montant`.
"""

from rest_framework import serializers


class ClientInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour la création ou la mise à jour d'un client.

    Champs acceptés :
        - nom (str)          : nom de famille
        - prenom (str)       : prénom
        - email (str)        : adresse email valide
        - telephone (str)    : numéro de téléphone
        - adresse (str)      : adresse postale
    """

    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=30)
    adresse = serializers.CharField()


class ClientOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie représentant un client.

    Inclut l'identifiant et le statut actif/inactif.
    """

    id = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    email = serializers.EmailField()
    telephone = serializers.CharField()
    adresse = serializers.CharField()
    est_actif = serializers.BooleanField()


class ContratInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour la création d'un contrat.

    Champs attendus :
        - client_id (UUID)   : identifiant du client
        - bien_id (UUID)     : identifiant du bien loué
        - date_debut (date)  : date de début de location
        - date_fin (date)    : date de fin de location
    """

    client_id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    date_debut = serializers.DateField()
    date_fin = serializers.DateField()


class ContratOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie pour un contrat.

    Le montant total est extrait du Value Object `Montant` via `source`.
    """

    id = serializers.UUIDField()
    client_id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    date_debut = serializers.DateField()
    date_fin = serializers.DateField()
    montant_total = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source='montant_total.valeur'
    )
    statut = serializers.CharField()