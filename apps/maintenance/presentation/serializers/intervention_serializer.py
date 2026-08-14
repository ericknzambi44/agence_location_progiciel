"""
Sérialiseurs pour l'API des interventions.

Gèrent la validation des données en entrée et la sérialisation en sortie.
Utilisent les attributs de l'entité domaine `Intervention`.
"""

from rest_framework import serializers


class InterventionInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la création / planification d'une intervention.
    """

    bien_id = serializers.UUIDField(help_text="UUID du bien concerné")
    technicien_id = serializers.UUIDField(help_text="UUID du technicien assigné")
    date_debut = serializers.DateTimeField(help_text="Date et heure de début")
    date_fin = serializers.DateTimeField(help_text="Date et heure de fin")
    description_panne = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Description optionnelle de la panne"
    )


class InterventionOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la réponse de détail / liste d'interventions.
    """

    id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField(source='technicien.id', read_only=True)
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    statut = serializers.CharField()
    cout_total = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        source='_cout_total',
        read_only=True
    )

    pieces_utilisees = serializers.SerializerMethodField()

    def get_pieces_utilisees(self, obj):
        """
        Construit une liste de dictionnaires représentant les pièces utilisées.
        """
        result = []
        for piece, quantite in obj.pieces_utilisees:
            result.append({
                'id': str(piece.id),
                'reference': piece.reference,
                'nom': piece.nom,
                'prix_unitaire': float(piece.prix_unitaire),
                'quantite': quantite
            })
        return result


class AjoutPieceSerializer(serializers.Serializer):
    """
    Sérialiseur pour l'ajout d'une pièce détachée à une intervention.
    """

    piece_id = serializers.UUIDField(help_text="UUID de la pièce à ajouter")
    quantite = serializers.IntegerField(min_value=1, help_text="Quantité (>= 1)")