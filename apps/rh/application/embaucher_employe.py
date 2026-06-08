from datetime import date
from decimal import Decimal
from shared_kernel.domain.value_objects import Email, PersonName
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from rh.domain.entities.employe import Employe
from rh.domain.repositories.employe_repository import EmployeRepository

class EmbaucherEmployeUseCase:
    def __init__(self, repo: EmployeRepository):
        self.repo = repo

    def execute(self, matricule_str: str, nom: str, prenom: str, email_str: str,
                date_embauche: date, taux_valeur: Decimal, poste: str) -> Employe:
        # Validation via VO
        matricule = Matricule(matricule_str)
        nom_vo = PersonName(nom)
        prenom_vo = PersonName(prenom)
        email_vo = Email(email_str)
        taux = TauxHoraire(taux_valeur)

        # Unicité
        if self.repo.get_by_email(email_vo):
            raise ValueError("Email déjà utilisé")
        if self.repo.get_by_matricule(matricule):
            raise ValueError("Matricule déjà utilisé")

        employe = Employe(
            matricule=matricule,
            nom=nom_vo,
            prenom=prenom_vo,
            email=email_vo,
            date_embauche=date_embauche,
            taux_horaire=taux,
            poste=poste
        )
        self.repo.add(employe)
        return employe