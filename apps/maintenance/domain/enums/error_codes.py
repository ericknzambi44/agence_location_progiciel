from enum import Enum

class InterventionError(Enum):
    INTERVENTION_SANS_TECHNICIEN = "L'intervention doit avoir un technicien affecté."
    INTERVENTION_SANS_BIEN = "L'intervention doit concerner au moins un bien."
    DATE_DEBUT_INFERIEURE_A_AUJOURD_HUI = "La date de début ne peut pas être dans le passé."
    DATE_FIN_AVANT_DATE_DEBUT = "La date de fin doit être postérieure à la date de début."
    INTERVENTION_DEJA_CLOTUREE = "Impossible de modifier une intervention clôturée."
    INTERVENTION_NON_PLANIFIEE = "L'intervention doit être planifiée avant d'être clôturée."

class PlanificationError(Enum):
    TECHNICIEN_INDISPONIBLE = "Le technicien n'est pas disponible sur la période demandée."
    CHEVAUCHEMENT_AVEC_AUTRE_INTERVENTION = "La plage horaire chevauche une autre intervention."
    BIEN_INDISPONIBLE_POUR_MAINTENANCE = "Le bien n'est pas dans un état permettant la maintenance."

class CalculCoutError(Enum):
    DUREE_NON_DEFINIE = "La durée de l'intervention n'est pas encore connue."
    TARIF_TECHNICIEN_NON_RENSEIGNE = "Le coût horaire du technicien n'est pas configuré."
    PIECES_DETACHEES_SANS_PRIX = "Certaines pièces détachées n'ont pas de prix unitaire."