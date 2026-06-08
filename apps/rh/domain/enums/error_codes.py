from enum import Enum

class EmployeError(Enum):
    EMAIL_EXISTANT = "Un employé avec cet email existe déjà."
    MATRICULE_EXISTANT = "Ce matricule est déjà attribué."
    EMPLOYE_INACTIF = "L'employé est inactif."
    EMPLOYE_INTROUVABLE = "Employé non trouvé."

class PointageError(Enum):
    DOUBLON_ENTREE = "Un pointage d'entrée existe déjà aujourd'hui sans sortie."
    SORTIE_SANS_ENTREE = "Impossible d'enregistrer une sortie sans entrée préalable."
    POINTAGE_HORS_PLAGE = "Le pointage est en dehors des horaires autorisés (optionnel)."

class EvaluationError(Enum):
    EVALUATION_TROP_RECENTE = "Une évaluation a déjà eu lieu il y a moins de 6 mois."
    NOTE_INVALIDE = "La note doit être comprise entre 0 et 10."

class RoleError(Enum):
    ROLE_INTROUVABLE = "Rôle non trouvé."
    PERMISSION_REFUSEE = "L'utilisateur n'a pas la permission requise."