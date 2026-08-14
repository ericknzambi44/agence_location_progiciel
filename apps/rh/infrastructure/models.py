"""
Modèles de données du module RH (Ressources Humaines).

Ce module gère :
    - Les employés (Employe) : identité, rattachement hiérarchique, agence, rôles
    - Les pointages (Pointage) : suivi des entrées/sorties
    - Les évaluations (Evaluation) : appréciation périodique des performances
    - Les rôles métier (Role) : définition de rôles applicatifs avec permissions JSON

Architecture :
    - Modèles Django (infrastructure) qui seront mappés vers les entités du domaine.
    - Utilisation de UUID comme clé primaire pour un référencement stable et distribué.
    - Séparation claire des préoccupations : les modèles n'ont pas de logique métier,
      uniquement la persistance et les relations.

Conventions :
    - Noms de classes au singulier (sans suffixe "Model") pour respecter les standards Django.
    - db_table explicite pour garder le contrôle des noms de tables.
    - Les relations sont définies avec `on_delete` approprié (PROTECT, CASCADE, etc.).
"""

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from administration.infrastructure.models import AgenceModel  # ✅ Import du modèle Agence
import uuid


class Employe(models.Model):
    """
    Représente un employé de l'entreprise.

    Un employé est lié :
        - à un utilisateur Django (compte de connexion) via OneToOneField, optionnel
        - à une agence (obligatoire) : il est rattaché à une entité géographique
        - à des groupes (rôles RBAC) pour déterminer ses permissions

    Champs :
        id (UUID)          : identifiant unique universel
        user (OneToOne)    : compte utilisateur Django associé (null si non créé)
        agence (FK)        : agence de rattachement (obligatoire)
        groups (M2M)       : rôles/groupes Django attribués à l'employé
        matricule (str)    : code unique interne de l'employé
        nom (str)          : nom de famille
        prenom (str)       : prénom
        email (str)        : adresse email professionnelle (unique)
        date_embauche (date) : date d'entrée dans l'entreprise
        taux_horaire (decimal) : rémunération horaire (peut être obsolète si salaire mensuel)
        poste (str)        : intitulé du poste occupé
        est_actif (bool)   : statut d'activité (True = en poste, False = sorti)

    Méthodes :
        save() : synchronise les groupes de l'utilisateur Django avec ceux de l'employé.
        clean() : valide les contraintes métier avant sauvegarde.
        __str__() : représentation lisible (matricule + nom complet).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employe_rh',
        null=True,
        blank=True,
        verbose_name="Compte utilisateur associé"
    )
    agence = models.ForeignKey(
        AgenceModel,  # ✅ Utilisation directe du modèle importé
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='employes',
        verbose_name="Agence de rattachement"
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        verbose_name="Rôles (groupes)"
    )
    matricule = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Matricule"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de famille"
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email"
    )
    date_embauche = models.DateField(
        verbose_name="Date d'embauche"
    )
    taux_horaire = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Taux horaire"
    )
    poste = models.CharField(
        max_length=100,
        verbose_name="Poste occupé"
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Est actif"
    )

    class Meta:
        db_table = 'rh_employe'
        app_label = 'rh'
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['matricule']
        indexes = [
            models.Index(fields=['matricule']),
            models.Index(fields=['agence', 'est_actif']),
        ]

    def clean(self):
        """
        Validation métier avant sauvegarde.
        """
        super().clean()
        # Vérifier que le matricule ne contient pas d'espaces et est en majuscules
        if self.matricule:
            self.matricule = self.matricule.strip().upper()
            if len(self.matricule) < 3:
                raise ValidationError({
                    'matricule': "Le matricule doit contenir au moins 3 caractères."
                })
        # Vérifier que l'email est en minuscules
        if self.email:
            self.email = self.email.lower()

    def save(self, *args, **kwargs):
        """
        Sauvegarde l'employé et synchronise les groupes de l'utilisateur lié.
        """
        self.full_clean()  # Appelle clean() avant save()
        super().save(*args, **kwargs)
        # Synchronisation des groupes avec l'utilisateur Django
        if self.user:
            self.user.groups.set(self.groups.all())
            self.user.is_active = self.est_actif
            self.user.save()

    def __str__(self):
        return f"{self.matricule} - {self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        """Retourne le nom complet (prénom + nom)."""
        return f"{self.prenom} {self.nom}".strip()


class Pointage(models.Model):
    """
    Représente un pointage d'entrée ou de sortie d'un employé.

    Champs :
        id (UUID)         : identifiant unique
        employe (FK)      : employé concerné (CASCADE : suppression du pointage si employé supprimé)
        horodatage (datetime) : date et heure du pointage
        type (str)        : 'ENTRY' pour entrée, 'EXIT' pour sortie
        commentaire (text) : remarque libre

    Contraintes :
        - Le type est limité aux valeurs 'ENTRY' et 'EXIT'.
        - Un employé ne peut pas avoir deux pointages de même type à la même seconde
          (contrainte d'unicité partielle appliquée en base via UniqueConstraint).
    """

    class TypePointage(models.TextChoices):
        ENTRY = 'ENTRY', 'Entrée'
        EXIT = 'EXIT', 'Sortie'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant"
    )
    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='pointages',
        verbose_name="Employé"
    )
    horodatage = models.DateTimeField(
        verbose_name="Date et heure du pointage"
    )
    type = models.CharField(
        max_length=5,
        choices=TypePointage.choices,
        verbose_name="Type de pointage"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )

    class Meta:
        db_table = 'rh_pointage'
        app_label = 'rh'
        verbose_name = "Pointage"
        verbose_name_plural = "Pointages"
        ordering = ['-horodatage']
        constraints = [
            models.UniqueConstraint(
                fields=['employe', 'horodatage', 'type'],
                name='unique_pointage_employe_horodatage_type'
            )
        ]
        indexes = [
            models.Index(fields=['employe', 'horodatage']),
        ]

    def clean(self):
        """
        Validation : s'assurer que l'horodatage n'est pas dans le futur.
        """
        super().clean()
        from django.utils import timezone
        if self.horodatage and self.horodatage > timezone.now():
            raise ValidationError({
                'horodatage': "L'horodatage ne peut pas être dans le futur."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employe.matricule} - {self.get_type_display()} - {self.horodatage}"


class Evaluation(models.Model):
    """
    Représente une évaluation périodique d'un employé.

    Champs :
        id (UUID)        : identifiant unique
        employe (FK)     : employé évalué
        date_evaluation (date) : date de l'évaluation
        note (decimal)   : note sur 10 (0.0 à 10.0)
        commentaires (text) : appréciations libres
        evaluateur_id (UUID) : identifiant de l'utilisateur qui a réalisé l'évaluation
                               (peut être un employé ou un chef, conservé en UUID simple)
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant"
    )
    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Employé évalué"
    )
    date_evaluation = models.DateField(
        verbose_name="Date d'évaluation"
    )
    note = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Note de 0.0 à 10.0",
        verbose_name="Note"
    )
    commentaires = models.TextField(
        blank=True,
        verbose_name="Commentaires"
    )
    evaluateur_id = models.UUIDField(
        null=True,
        blank=True,
        verbose_name="Identifiant de l'évaluateur"
    )

    class Meta:
        db_table = 'rh_evaluation'
        app_label = 'rh'
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        ordering = ['-date_evaluation']
        constraints = [
            models.CheckConstraint(
                check=models.Q(note__gte=0) & models.Q(note__lte=10),
                name='note_entre_0_et_10'
            )
        ]
        indexes = [
            models.Index(fields=['employe', 'date_evaluation']),
        ]

    def clean(self):
        """
        Validation : la note doit être comprise entre 0 et 10.
        """
        super().clean()
        if self.note is not None and (self.note < 0 or self.note > 10):
            raise ValidationError({
                'note': "La note doit être comprise entre 0.0 et 10.0."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Éval. {self.employe.matricule} - {self.date_evaluation}"


class Role(models.Model):
    """
    Représente un rôle métier applicatif.

    Ce modèle est distinct des groupes Django (`auth.Group`) et permet de
    définir des rôles applicatifs avec des permissions stockées sous forme JSON.
    Il offre une flexibilité pour des permissions spécifiques au métier
    (ex: "valider_pointage", "approuver_conge", etc.) qui ne correspondent pas
    forcément aux permissions CRUD standard de Django.

    Champs :
        id (UUID)       : identifiant unique
        nom (str)       : nom unique du rôle (ex: "Chef de service", "Gestionnaire RH")
        permissions (JSON) : liste des codes de permissions métier, ex:
                             ["view_employe", "add_pointage", "approve_conge"]
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant"
    )
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du rôle"
    )
    permissions = models.JSONField(
        default=list,
        help_text="Liste des codes de permissions métier (ex: ['view_employe', 'add_pointage'])",
        verbose_name="Permissions"
    )

    class Meta:
        db_table = 'rh_role'
        app_label = 'rh'
        verbose_name = "Rôle métier"
        verbose_name_plural = "Rôles métier"
        ordering = ['nom']

    def clean(self):
        """
        Validation : le nom ne doit pas être vide, les permissions doivent être une liste.
        """
        super().clean()
        if not self.nom or not self.nom.strip():
            raise ValidationError({
                'nom': "Le nom du rôle ne peut pas être vide."
            })
        if not isinstance(self.permissions, list):
            raise ValidationError({
                'permissions': "Les permissions doivent être une liste."
            })
        # Vérifier que chaque permission est une chaîne non vide
        for perm in self.permissions:
            if not isinstance(perm, str) or not perm.strip():
                raise ValidationError({
                    'permissions': "Chaque permission doit être une chaîne non vide."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom