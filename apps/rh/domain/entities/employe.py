"""
Entité domaine Employe.

Représente un employé avec ses informations personnelles, son agence,
ses rôles (via group_ids) et ses méthodes métier.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from shared_kernel.domain.value_objects import Email, PersonName


@dataclass
class Employe:
    """
    Entité Employe.

    Attributes:
        matricule (Matricule): Matricule unique.
        nom (PersonName): Nom de famille.
        prenom (PersonName): Prénom.
        email (Email): Adresse email professionnelle.
        date_embauche (date): Date d'embauche.
        taux_horaire (TauxHoraire): Taux horaire.
        poste (str): Poste occupé.
        role_id (UUID, optionnel): Ancien identifiant de rôle (obsolète, voir group_ids).
        agence_id (UUID, optionnel): Identifiant de l'agence de rattachement.
        est_actif (bool): Statut d'activité.
        id (UUID): Identifiant unique.
        group_ids (List[UUID]): Liste des identifiants de groupes Django (RBAC).
    """

    matricule: Matricule
    nom: PersonName
    prenom: PersonName
    email: Email
    date_embauche: date
    taux_horaire: TauxHoraire
    poste: str
    role_id: Optional[UUID] = None
    agence_id: Optional[UUID] = None
    est_actif: bool = True
    id: UUID = field(default_factory=uuid4)
    group_ids: List[UUID] = field(default_factory=list)

    def __post_init__(self):
        """
        Validations après initialisation.
        """
        if self.date_embauche > date.today():
            raise ValueError("La date d'embauche ne peut pas être dans le futur.")
        if not self.poste or not self.poste.strip():
            raise ValueError("Le poste est obligatoire.")

    def desactiver(self):
        """Désactive l'employé (soft delete)."""
        self.est_actif = False

    def reactiver(self):
        """Réactive l'employé."""
        self.est_actif = True