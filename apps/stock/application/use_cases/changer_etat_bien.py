"""
Use case pour changer l'état d'un bien.

Valide la transition d'état via l'entité métier et persiste le bien,
en tenant compte de l'agence pour l'isolation.
"""

from uuid import UUID

from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.repositories.bien_repository import BienRepository


class ChangerEtatBienUseCase:
    """
    Use case pour modifier l'état d'un bien.

    Args:
        repo (BienRepository): Repository pour la persistance des biens.
    """

    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, bien_id: UUID, nouvel_etat: str, agence_id: UUID = None) -> None:
        """
        Exécute le changement d'état d'un bien.

        Args:
            bien_id (UUID): Identifiant du bien.
            nouvel_etat (str): Nouvel état souhaité.
            agence_id (UUID, optional): Agence pour l'isolation.

        Raises:
            ValueError: Si le bien n'existe pas, si l'état est invalide,
                        ou si la transition n'est pas autorisée.
        """
        # 1. Récupération du bien, filtré par agence si fournie
        bien = self.repo.get(bien_id, agence_id=agence_id)
        if not bien:
            raise ValueError("Bien non trouvé ou non autorisé pour votre agence.")

        # 2. Conversion de l'état en Enum
        try:
            etat_enum = EtatBien(nouvel_etat)
        except ValueError:
            raise ValueError(
                f"État invalide : {nouvel_etat}. Valeurs autorisées : {[e.value for e in EtatBien]}"
            )

        # 3. Application de la transition métier via l'entité
        if etat_enum == EtatBien.EN_MAINTENANCE:
            bien.passer_en_maintenance()
        elif etat_enum == EtatBien.DISPONIBLE:
            bien.liberer_apres_maintenance()
        elif etat_enum == EtatBien.ENDOMMAGE:
            bien.signaler_endommagement()
        elif etat_enum == EtatBien.ARCHIVE:
            bien.archiver()
        else:
            raise ValueError(f"État non supporté : {nouvel_etat}")

        # 4. Persistance
        self.repo.update(bien)