from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import TechnicienModel
from shared_kernel.domain.value_objects import Email, PersonName

class TechnicienMapper:
    @staticmethod
    def to_domain(model: TechnicienModel) -> Technicien:
        return Technicien(
            id=model.id,
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            cout_horaire=model.cout_horaire,
            est_actif=True
        )

    @staticmethod
    def to_model(entity: Technicien) -> TechnicienModel:
        return TechnicienModel(
            id=entity.id,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            cout_horaire=entity.cout_horaire
        )