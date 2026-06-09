from decimal import Decimal
from rh.domain.entities.employe import Employe
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from shared_kernel.domain.value_objects import Email, PersonName
from rh.infrastructure.models import EmployeModel

class EmployeMapper:
    @staticmethod
    def to_domain(model: EmployeModel) -> Employe:
        return Employe(
            id=model.id,
            matricule=Matricule(model.matricule),
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            date_embauche=model.date_embauche,
            taux_horaire=TauxHoraire(Decimal(str(model.taux_horaire))),  # conversion correcte
            poste=model.poste,
            est_actif=model.est_actif,
            role_id=model.role_id
        )

    @staticmethod
    def to_model(entity: Employe) -> EmployeModel:
        return EmployeModel(
            id=entity.id,
            matricule=entity.matricule.value,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            date_embauche=entity.date_embauche,
            taux_horaire=entity.taux_horaire.valeur,
            poste=entity.poste,
            est_actif=entity.est_actif,
            role_id=entity.role_id
        )