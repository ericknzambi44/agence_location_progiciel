from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import TechnicienModel
from shared_kernel.domain.value_objects import Email, PersonName
from decimal import Decimal

class TechnicienMapper:
    @staticmethod
    def to_domain(model: TechnicienModel) -> Technicien:
        return Technicien(
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            cout_horaire=Decimal(str(model.cout_horaire)),
            actif=True,  # valeur par défaut car le modèle n'a pas ce champ
            id=model.id
        )

    @staticmethod
    def to_model(entity: Technicien) -> TechnicienModel:
        return TechnicienModel(
            id=entity.id,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            cout_horaire=entity.cout_horaire
            # pas de champ actif dans le modèle
        )