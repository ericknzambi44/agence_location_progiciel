from administration.domain.entities.agence import Agence
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email
from administration.infrastructure.models import AgenceModel

class AgenceMapper:
    @staticmethod
    def to_domain(model: AgenceModel) -> Agence:
        adresse = Adresse(
            rue=model.adresse_ligne1,
            code_postal=model.code_postal,
            ville=model.ville,
            pays=model.pays
        )
        telephone = Telephone(model.telephone)
        email = Email(model.email)
        code = CodeAgence(model.code)

        return Agence(
            id=model.id,
            code=code,
            nom=model.nom,
            adresse=adresse,
            telephone=telephone,
            email=email,
            actif=model.actif,
            date_creation=model.date_creation
        )

    @staticmethod
    def to_model(entity: Agence) -> AgenceModel:
        return AgenceModel(
            id=entity.id,
            code=entity.code.value,
            nom=entity.nom,
            adresse_ligne1=entity.adresse.rue,
            adresse_ligne2="",
            code_postal=entity.adresse.code_postal,
            ville=entity.adresse.ville,
            pays=entity.adresse.pays,
            telephone=entity.telephone.value,
            email=entity.email.value,
            actif=entity.actif,
            date_creation=entity.date_creation
        )