import uuid
from administration.domain.entities.agence import Agence
from administration.domain.value_objects.adresse import Adresse
from administration.domain.value_objects.telephone import Telephone
from administration.domain.value_objects.code_agence import CodeAgence
from shared_kernel.domain.value_objects import Email
from administration.domain.repositories.agence_repository import AgenceRepository

class CreerAgenceUseCase:
    def __init__(self, repo: AgenceRepository):
        self.repo = repo

    def execute(self, nom: str, adresse_ligne1: str, adresse_ligne2: str,
                code_postal: str, ville: str, pays: str, telephone: str, email: str) -> Agence:
        # Génération d'un code valide : 6 caractères hexadécimaux majuscules
        code_value = uuid.uuid4().hex[:6].upper()
        code = CodeAgence(code_value)
        adresse = Adresse(rue=adresse_ligne1, code_postal=code_postal, ville=ville, pays=pays)
        tel = Telephone(telephone)
        email_vo = Email(email)

        if self.repo.get_by_nom(nom):
            raise ValueError("Une agence avec ce nom existe déjà.")

        agence = Agence(code=code, nom=nom, adresse=adresse, telephone=tel, email=email_vo)
        self.repo.add(agence)
        return agence