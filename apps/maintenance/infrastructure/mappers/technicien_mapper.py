"""
Mapper entre l'entité domaine Technicien et le modèle ORM Technicien.

Assure la conversion bidirectionnelle, incluant l'agence_id pour le multi-agences.
"""

from maintenance.domain.entities.technicien import Technicien
from maintenance.infrastructure.models import Technicien as TechnicienModel  # alias
from shared_kernel.domain.value_objects import Email, PersonName


class TechnicienMapper:
    """Conversion bidirectionnelle pour les techniciens."""

    @staticmethod
    def to_domain(model: TechnicienModel) -> Technicien:
        """
        Construit une entité Technicien à partir du modèle Django.

        Returns:
            Technicien: Entité domaine.
        """
        return Technicien(
            id=model.id,
            nom=PersonName(model.nom),
            prenom=PersonName(model.prenom),
            email=Email(model.email),
            cout_horaire=model.cout_horaire,
            agence_id=model.agence_id,
            est_actif=True
        )

    @staticmethod
    def to_model(entity: Technicien) -> TechnicienModel:
        """
        Construit un modèle Django à partir de l'entité Technicien.

        Returns:
            TechnicienModel: Instance ORM non persistée.
        """
        return TechnicienModel(
            id=entity.id,
            nom=entity.nom.value,
            prenom=entity.prenom.value,
            email=entity.email.value,
            cout_horaire=entity.cout_horaire,
            agence_id=entity.agence_id
        )