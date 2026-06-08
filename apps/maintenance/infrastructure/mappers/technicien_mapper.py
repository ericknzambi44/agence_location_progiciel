from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import TechnicienModel
from shared_kernel.domain.value_objects.email import Email
from shared_kernel.domain.value_objects.name import PersonName

class TechnicienMapper:
    @staticmethod
    def to_domain(model: TechnicienModel) -> Technicien:
        return Technicien(
            id=model.id,
            nom=PersonName(model.nom),
            email=Email(model.email),
            specialite=model.specialite,
            cout_horaire=float(model.cout_horaire)
        )

    @staticmethod
    def to_model(entity: Technicien) -> TechnicienModel:
        return TechnicienModel(
            id=entity.id,
            nom=str(entity.nom),
            email=str(entity.email),
            specialite=entity.specialite,
            cout_horaire=entity.cout_horaire
        )