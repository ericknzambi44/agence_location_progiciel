"""
Use case pour changer l'état d'un bien.
Valide la transition d'état via l'entité métier et persiste le bien.
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

    def execute(self, bien_id: UUID, nouvel_etat: str) -> None:
        """
        Exécute le changement d'état d'un bien.

        Args:
            bien_id (UUID): Identifiant du bien.
            nouvel_etat (str): Nouvel état souhaité ('disponible', 'en_maintenance', 'endommage', 'archive').

        Raises:
            ValueError: Si le bien n'existe pas, si l'état est invalide, ou si la transition n'est pas autorisée.
        """
        # 1. Récupération du bien
        bien = self.repo.get(bien_id)
        if not bien:
            raise ValueError("Bien non trouvé.")

        # 2. Conversion de l'état en Enum
        try:
            etat_enum = EtatBien(nouvel_etat)
        except ValueError:
            raise ValueError(f"État invalide : {nouvel_etat}. Valeurs autorisées : {[e.value for e in EtatBien]}")

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
            # Normalement déjà capturé par la conversion en Enum
            raise ValueError(f"État non supporté : {nouvel_etat}")

        # 4. Persistance
        self.repo.update(bien)