from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date
from decimal import Decimal
from shared_kernel.domain.value_objects import Email, PersonName
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from typing import Optional

@dataclass
class Employe:
    id: UUID = field(default_factory=uuid4)
    matricule: Matricule
    nom: PersonName
    prenom: PersonName
    email: Email
    date_embauche: date
    taux_horaire: TauxHoraire
    poste: str
    est_actif: bool = True
    role_id: Optional[UUID] = None   # lien vers Role (RBAC)

    def __post_init__(self):
        if self.date_embauche > date.today():
            raise ValueError("La date d'embauche ne peut pas être dans le futur.")
        if not self.poste or not self.poste.strip():
            raise ValueError("Le poste est obligatoire.")

    def desactiver(self):
        self.est_actif = False

    def reactiver(self):
        self.est_actif = True