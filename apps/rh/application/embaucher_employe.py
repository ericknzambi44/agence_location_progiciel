"""
Use case pour embaucher un employé.
Valide les données, vérifie l'unicité de l'email et du matricule,
assigne l'agence_id et persiste l'employé.
"""
from datetime import date
from decimal import Decimal
from uuid import UUID

from shared_kernel.domain.value_objects import Email, PersonName
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from rh.domain.entities.employe import Employe
from rh.domain.repositories.employe_repository import EmployeRepository


class EmbaucherEmployeUseCase:
    """
    Use case pour embaucher un nouvel employé.
    """

    def __init__(self, repo: EmployeRepository):
        self.repo = repo

    def execute(self, matricule_str: str, nom: str, prenom: str, email_str: str,
                date_embauche: date, taux_valeur: Decimal, poste: str,
                agence_id: UUID = None) -> Employe:
        """
        Exécute l'embauche d'un employé.

        Args:
            matricule_str (str): Matricule unique.
            nom (str): Nom de famille.
            prenom (str): Prénom.
            email_str (str): Email (unique).
            date_embauche (date): Date d'embauche.
            taux_valeur (Decimal): Taux horaire.
            poste (str): Poste occupé.
            agence_id (UUID): Identifiant de l'agence. Obligatoire.

        Returns:
            Employe: L'entité employé créée.

        Raises:
            ValueError: Si l'email ou le matricule est déjà utilisé,
                        ou si agence_id est manquant.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour embaucher un employé.")

        # 1. Validation via Value Objects
        matricule = Matricule(matricule_str)
        nom_vo = PersonName(nom)
        prenom_vo = PersonName(prenom)
        email_vo = Email(email_str)
        taux = TauxHoraire(taux_valeur)

        # 2. Vérification de l'unicité (global ou par agence ? Ici on garde global pour l'email/matricule)
        if self.repo.get_by_email(email_vo):
            raise ValueError("Email déjà utilisé")
        if self.repo.get_by_matricule(matricule):
            raise ValueError("Matricule déjà utilisé")

        # 3. Construction de l'entité
        employe = Employe(
            matricule=matricule,
            nom=nom_vo,
            prenom=prenom_vo,
            email=email_vo,
            date_embauche=date_embauche,
            taux_horaire=taux,
            poste=poste,
            agence_id=agence_id   # <-- assignation de l'agence
        )

        # 4. Persistance
        self.repo.add(employe)

        return employe