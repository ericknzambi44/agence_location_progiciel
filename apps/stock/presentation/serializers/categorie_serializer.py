"""
Sérialiseurs REST pour l'entité Categorie.

Ils sont déclaratifs et basés sur les champs de l'entité domaine `Categorie`.
"""

from rest_framework import serializers


class CategorieInputSerializer(serializers.Serializer):
    """
    Sérialiseur d'entrée pour créer ou modifier une catégorie.

    Champs acceptés :
        - nom (str)          : nom de la catégorie (obligatoire)
        - description (str)  : description optionnelle
        - parent (UUID)      : identifiant de la catégorie parente (optionnel)
    """

    nom = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    parent = serializers.UUIDField(required=False, allow_null=True)


class CategorieOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie d'une catégorie.
    """

    id = serializers.UUIDField()
    nom = serializers.CharField()
    description = serializers.CharField(required=False)
    parent = serializers.UUIDField(required=False, allow_null=True)