"""
Mapper entre l'entité Agence et le modèle Django AgenceModel.
"""
from administration.domain.entities.agence import Agence
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email
from administration.infrastructure.models import AgenceModel


class AgenceMapper:
    @staticmethod
    def to_domain(model: AgenceModel) -> Agence:
        """
        Convertit un modèle Django en entité Agence.
        """
        adresse = Adresse(
            ligne1=model.adresse_ligne1,
            ligne2=model.adresse_ligne2 or "",
            code_postal=model.code_postal or "",
            ville=model.ville,
            pays=model.pays
        )
        tel = Telephone(model.telephone)
        email = Email(model.email)
        code = CodeAgence(model.code) if model.code else None

        return Agence(
            id=model.id,
            code=code,
            nom=model.nom,
            adresse=adresse,
            telephone=tel,
            email=email,
            actif=model.actif,
            date_creation=model.date_creation
        )

    @staticmethod
    def to_model(entity: Agence) -> AgenceModel:
        """
        Convertit une entité Agence en modèle Django.
        """
        return AgenceModel(
            id=entity.id,
            code=entity.code.value if entity.code else "",
            nom=entity.nom,
            adresse_ligne1=entity.adresse.ligne1,
            adresse_ligne2=entity.adresse.ligne2,
            code_postal=entity.adresse.code_postal,
            ville=entity.adresse.ville,
            pays=entity.adresse.pays,
            telephone=entity.telephone.value,
            email=entity.email.value,
            actif=entity.actif,
            date_creation=entity.date_creation
        )