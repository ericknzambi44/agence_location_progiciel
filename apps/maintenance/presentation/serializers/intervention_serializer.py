"""
Sérialiseurs pour l'API des interventions.
Gèrent la validation des données en entrée et la sérialisation en sortie.
"""
from rest_framework import serializers

class InterventionInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la création / planification d'une intervention.
    Tous les champs sont obligatoires (sauf description_panne).
    """
    bien_id = serializers.UUIDField(help_text="UUID du bien concerné")
    technicien_id = serializers.UUIDField(help_text="UUID du technicien assigné")
    date_debut = serializers.DateTimeField(help_text="Date et heure de début (format ISO)")
    date_fin = serializers.DateTimeField(help_text="Date et heure de fin (format ISO)")
    description_panne = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Description optionnelle de la panne"
    )


class InterventionOutputSerializer(serializers.Serializer):
    """
    Sérialiseur pour la réponse de détail / liste d'interventions.
    Inclut les informations de l'intervention et son coût total.
    """
    id = serializers.UUIDField()
    bien_id = serializers.UUIDField()
    technicien_id = serializers.UUIDField(source='technicien.id', read_only=True)
    date_debut = serializers.DateTimeField()
    date_fin = serializers.DateTimeField()
    statut = serializers.CharField()
    cout_total = serializers.DecimalField(max_digits=12, decimal_places=2, source='_cout_total', read_only=True)

    # Ajout du champ pieces_utilisees pour afficher les pièces en détail
    pieces_utilisees = serializers.SerializerMethodField()

    def get_pieces_utilisees(self, obj):
        """
        Construit une liste de dictionnaires représentant les pièces utilisées.
        Chaque dictionnaire contient l'identifiant, la référence, le nom, le prix unitaire et la quantité.
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

    @staticmethod
    def from_entity(intervention):
        """
        Méthode utilitaire pour construire un dictionnaire à partir d'une entité Intervention.
        Utilisée pour les réponses personnalisées ou les tests.
        """
        return {
            'id': str(intervention.id),
            'bien_id': str(intervention.bien_id),
            'technicien_id': str(intervention.technicien.id) if intervention.technicien else None,
            'date_debut': intervention.date_debut.isoformat() if intervention.date_debut else None,
            'date_fin': intervention.date_fin.isoformat() if intervention.date_fin else None,
            'statut': intervention.statut,
            'cout_total': float(intervention._cout_total) if hasattr(intervention, '_cout_total') else 0.0,
            'pieces_utilisees': [
                {
                    'id': str(piece.id),
                    'reference': piece.reference,
                    'nom': piece.nom,
                    'prix_unitaire': float(piece.prix_unitaire),
                    'quantite': quantite
                }
                for piece, quantite in intervention.pieces_utilisees
            ]
        }


class AjoutPieceSerializer(serializers.Serializer):
    """
    Sérialiseur pour l'ajout d'une pièce détachée à une intervention.
    """
    piece_id = serializers.UUIDField(help_text="UUID de la pièce à ajouter")
    quantite = serializers.IntegerField(min_value=1, help_text="Quantité à ajouter (>= 1)")