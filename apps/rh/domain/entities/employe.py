from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from shared_kernel.domain.value_objects import Email, PersonName
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire

@dataclass
class Employe:
    matricule: Matricule
    nom: PersonName
    prenom: PersonName
    email: Email
    date_embauche: date
    taux_horaire: TauxHoraire
    poste: str
    est_actif: bool = True
    role_id: UUID = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.date_embauche > date.today():
            raise ValueError("La date d'embauche ne peut pas être dans le futur.")
        if not self.poste or not self.poste.strip():
            raise ValueError("Le poste est obligatoire.")