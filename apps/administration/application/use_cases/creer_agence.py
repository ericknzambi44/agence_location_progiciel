from administration.domain.entities.agence import Agence
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email
from administration.domain.repositories.agence_repository import AgenceRepository
from uuid import uuid4


class CreerAgenceUseCase:
    def __init__(self, repo: AgenceRepository):
        self.repo = repo

    def execute(self, nom: str, adresse_ligne1: str, adresse_ligne2: str,
                code_postal: str, ville: str, pays: str, telephone: str, email: str) -> Agence:
        # Création du Value Object Adresse avec les bons paramètres
        adresse = Adresse(
            ligne1=adresse_ligne1,
            ligne2=adresse_ligne2,
            code_postal=code_postal,
            ville=ville,
            pays=pays
        )
        tel = Telephone(telephone)
        email_vo = Email(email)

        # Génération d'un code simple (peut être amélioré)
        code = CodeAgence(nom[:5].upper() + uuid4().hex[:3].upper())

        # Vérifier l'unicité du nom
        if self.repo.get_by_nom(nom):
            raise ValueError("Une agence avec ce nom existe déjà.")

        agence = Agence(
            code=code,
            nom=nom,
            adresse=adresse,
            telephone=tel,
            email=email_vo
        )
        self.repo.add(agence)
        return agence