"""
Sérialiseurs REST pour la gestion des stocks et des mouvements.

Ce module contient :
    - NiveauStockOutputSerializer : sortie du niveau de stock d'un article
    - MouvementStockInputSerializer : entrée pour créer un mouvement
    - MouvementStockOutputSerializer : sortie d'un mouvement

Ces sérialiseurs sont déclaratifs et indépendants des modèles Django
(approche Clean Architecture). Ils manipulent des entités du domaine.
"""

from rest_framework import serializers

from stock.domain.value_objects.type_mouvement import TypeMouvement


class NiveauStockOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie pour le niveau de stock d'un article.

    Champs :
        - article_id (UUID) : identifiant de l'article
        - quantite_disponible (int) : quantité disponible en stock
        - nom (str) : nom de l'article (optionnel, si fourni par le repository)
        - reference (str) : référence de l'article (optionnel)
    """

    article_id = serializers.UUIDField()
    quantite_disponible = serializers.IntegerField()
    nom = serializers.CharField(required=False, allow_blank=True)
    reference = serializers.CharField(required=False, allow_blank=True)


class MouvementStockInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour l'enregistrement d'un mouvement de stock.

    Champs attendus :
        - article_id (UUID) : identifiant de l'article concerné
        - type_mouvement (str) : 'entree', 'sortie', 'retour', etc.
        - quantite (int) : quantité positive
        - motif (str) : motif du mouvement (optionnel)
    """

    article_id = serializers.UUIDField(
        help_text="Identifiant de l'article concerné."
    )
    type_mouvement = serializers.ChoiceField(
        choices=[e.value for e in TypeMouvement],
        help_text="Type de mouvement : entree, sortie, retour, ajustement, etc."
    )
    quantite = serializers.IntegerField(
        min_value=1,
        help_text="Quantité concernée (strictement positive)."
    )
    motif = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Motif ou commentaire du mouvement."
    )


class MouvementStockOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie pour un mouvement de stock.

    Champs :
        - id (UUID) : identifiant du mouvement
        - article_id (UUID) : article concerné
        - type_mouvement (str) : type du mouvement
        - quantite (int) : quantité
        - motif (str) : motif
        - date_heure (datetime) : date et heure du mouvement
    """

    id = serializers.UUIDField()
    article_id = serializers.UUIDField(source='article_id')
    type_mouvement = serializers.CharField(source='type_mouvement.value')
    quantite = serializers.IntegerField()
    motif = serializers.CharField(required=False, allow_blank=True)
    date_heure = serializers.DateTimeField()