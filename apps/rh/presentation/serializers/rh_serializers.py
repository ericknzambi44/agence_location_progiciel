"""
Sérialiseurs REST pour le module Ressources Humaines (RH).

Ce module contient les sérialiseurs d'entrée et de sortie utilisés par
les endpoints de gestion des employés, des pointages, et du profil
utilisateur connecté.

Les sérialiseurs de sortie utilisent `source` pour extraire correctement
les valeurs des Value Objects (ex: `matricule.value`, `taux_horaire.valeur`).
"""

from rest_framework import serializers

# ------------------------------------------------------------------------------
# 1. Sérialiseurs liés aux employés
# ------------------------------------------------------------------------------


class EmployeInputSerializer(serializers.Serializer):
    """
    Sérialiseur de création / mise à jour d'un employé.
    """

    matricule = serializers.CharField(
        max_length=10,
        help_text="Matricule unique de l'employé dans l'entreprise.",
    )
    nom = serializers.CharField(
        max_length=100,
        help_text="Nom de famille de l'employé.",
    )
    prenom = serializers.CharField(
        max_length=100,
        help_text="Prénom de l'employé.",
    )
    email = serializers.EmailField(
        help_text="Adresse email professionnelle de l'employé.",
    )
    date_embauche = serializers.DateField(
        help_text="Date d'entrée en fonction (YYYY-MM-DD).",
    )
    taux_horaire = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Taux horaire brut en devise locale.",
    )
    poste = serializers.CharField(
        max_length=100,
        help_text="Intitulé du poste occupé.",
    )


class EmployeOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie représentant un employé.
    Mappe directement les champs de l'entité domaine `Employe` en extrayant
    les valeurs internes des Value Objects.
    """

    id = serializers.UUIDField(help_text="Identifiant unique de l'employé.")
    matricule = serializers.CharField(
        source='matricule.value',
        help_text="Matricule de l'employé."
    )
    nom = serializers.CharField(
        source='nom.value',
        help_text="Nom de famille."
    )
    prenom = serializers.CharField(
        source='prenom.value',
        help_text="Prénom."
    )
    email = serializers.EmailField(
        source='email.value',
        help_text="Adresse email."
    )
    date_embauche = serializers.DateField(help_text="Date d'embauche.")
    taux_horaire = serializers.DecimalField(
        source='taux_horaire.valeur',
        max_digits=8,
        decimal_places=2,
        help_text="Taux horaire.",
    )
    poste = serializers.CharField(help_text="Poste occupé.")
    est_actif = serializers.BooleanField(
        help_text="Indique si l'employé est toujours en activité."
    )


# ------------------------------------------------------------------------------
# 2. Sérialiseurs liés aux pointages
# ------------------------------------------------------------------------------


class PointageInputSerializer(serializers.Serializer):
    """
    Sérialiseur pour l'enregistrement d'un pointage (entrée ou sortie).
    """

    employe_id = serializers.UUIDField(
        help_text="Identifiant de l'employé concerné."
    )
    type = serializers.ChoiceField(
        choices=["ENTRY", "EXIT"],
        help_text="Type de pointage : ENTRY (entrée) ou EXIT (sortie).",
    )
    horodatage = serializers.DateTimeField(
        required=False,
        help_text="Horodatage du pointage (optionnel, prend la date/heure "
        "courante si non fourni).",
    )


class PointageOutputSerializer(serializers.Serializer):
    """
    Sérialiseur de sortie d'un pointage.
    """

    id = serializers.UUIDField(help_text="Identifiant unique du pointage.")
    employe_id = serializers.UUIDField(
        source='employe.id',
        help_text="Identifiant de l'employé pointé."
    )
    horodatage = serializers.DateTimeField(help_text="Date et heure du pointage.")
    type = serializers.CharField(help_text="'ENTRY' ou 'EXIT'.")


# ------------------------------------------------------------------------------
# 3. Sérialiseurs pour l'authentification et le profil connecté
# ------------------------------------------------------------------------------


class UserSerializer(serializers.Serializer):
    """
    Représentation légère de l'utilisateur Django (compte de connexion).
    Utilisé dans la réponse /api/auth/me/ pour identifier le compte lié.
    """

    id = serializers.IntegerField(help_text="ID de l'utilisateur Django.")
    username = serializers.CharField(help_text="Nom d'utilisateur.")
    email = serializers.EmailField(help_text="Adresse email du compte.")


class EmployeMeSerializer(serializers.Serializer):
    """
    Informations détaillées de l'employé connecté.
    Inclut les données de base, l'agence et l'utilisateur lié.

    Note : l'entité domaine `Employe` ne possède pas directement d'attribut
    `user`. Pour l'instant, on omet ce champ ou on l'ajoute plus tard si nécessaire.
    """

    id = serializers.UUIDField(help_text="UUID de l'employé.")
    # user = UserSerializer(help_text="Compte utilisateur associé.")  # <-- retiré
    matricule = serializers.CharField(
        source='matricule.value',
        help_text="Matricule."
    )
    nom = serializers.CharField(
        source='nom.value',
        help_text="Nom de famille."
    )
    prenom = serializers.CharField(
        source='prenom.value',
        help_text="Prénom."
    )
    email = serializers.EmailField(
        source='email.value',
        help_text="Email professionnel."
    )
    poste = serializers.CharField(help_text="Poste occupé.")
    agence_id = serializers.UUIDField(
        help_text="Identifiant de l'agence de rattachement."
    )
    agence_nom = serializers.SerializerMethodField(
        help_text="Nom de l'agence de rattachement (si disponible)."
    )
    est_actif = serializers.BooleanField(help_text="L'employé est-il actif ?")

    def get_agence_nom(self, obj):
        """
        Tente de retourner le nom de l'agence à partir de l'entité Employe.
        Pour l'instant, l'entité ne contient que `agence_id`, donc on renvoie None.
        On pourra enrichir plus tard si le nom est injecté dans l'entité.
        """
        return None


class MeSerializer(serializers.Serializer):
    """
    Réponse de l'endpoint /api/auth/me/.
    Fournit le profil complet de l'employé connecté et la liste de
    ses permissions (RBAC) déduites des groupes Django.
    """

    employe = EmployeMeSerializer(help_text="Données de l'employé connecté.")
    permissions = serializers.ListField(
        child=serializers.CharField(),
        help_text="Liste des permissions (ex: 'app.view_sales').",
    )