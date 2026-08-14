"""
Mapper Employe : convertit entre le modèle Django `Employe` et l'entité domaine `Employe`.

Ce mapper fait partie de la couche infrastructure (persistance) et respecte
la séparation Clean Architecture : il traduit les objets de persistance
en objets du domaine, et inversement.

Note :
    L'affectation des groupes (M2M) ne peut pas être réalisée directement
    lors de la création d'un objet `Employe` non sauvegardé. Le repository
    est responsable d'effectuer `employe_model.groups.set(entity.group_ids)`
    après la sauvegarde.
"""

from decimal import Decimal
from typing import List
from uuid import UUID

from rh.domain.entities.employe import Employe
from rh.domain.value_objects.matricule import Matricule
from rh.domain.value_objects.taux_horaire import TauxHoraire
from shared_kernel.domain.value_objects import Email, PersonName
from rh.infrastructure.models import Employe as EmployeModel  # alias pour clarté


class EmployeMapper:
    """
    Convertit les objets entre le modèle de persistance `Employe`
    et l'entité du domaine `Employe`.
    """

    @staticmethod
    def to_domain(model: EmployeModel) -> Employe:
        """
        Convertit une instance `Employe` (modèle Django) en entité domaine.

        Args:
            model (EmployeModel): Instance du modèle ORM.

        Returns:
            Employe: Entité domaine correspondante, avec les groupes.
        """
        # Récupération des identifiants des groupes (M2M)
        group_ids: List[UUID] = list(model.groups.values_list('id', flat=True))

        return Employe(
            id=model.id,
            matricule=Matricule(model.matricule),
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            date_embauche=model.date_embauche,
            taux_horaire=TauxHoraire(Decimal(str(model.taux_horaire))),
            poste=model.poste,
            est_actif=model.est_actif,
            agence_id=model.agence_id,
            group_ids=group_ids,
        )

    @staticmethod
    def to_model(entity: Employe) -> EmployeModel:
        """
        Convertit une entité domaine `Employe` en instance du modèle Django.

        Attention : cette méthode ne sauvegarde pas l'objet et n'affecte pas
        les groupes (M2M). Le repository devra appeler `save()` puis
        `groups.set(entity.group_ids)`.

        Args:
            entity (Employe): Entité domaine à convertir.

        Returns:
            EmployeModel: Instance du modèle ORM (non persistée).
        """
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
            agence_id=entity.agence_id,
        )