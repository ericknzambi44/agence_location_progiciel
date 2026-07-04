from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional

from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from shared_kernel.domain.value_objects import Email, PersonName


@dataclass
class Employe:
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

    def __post_init__(self):
        if self.date_embauche > date.today():
            raise ValueError("La date d'embauche ne peut pas être dans le futur.")
        if not self.poste or not self.poste.strip():
            raise ValueError("Le poste est obligatoire.")

    def desactiver(self):
        self.est_actif = False

    def reactiver(self):
        self.est_actif = True