from uuid import UUID
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import EtatBien

class ChangerEtatBienUseCase:
    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, bien_id: UUID, nouvel_etat: str):
        bien = self.repo.get(bien_id)
        if not bien:
            raise ValueError("Bien introuvable")
        # Utilisation des méthodes métier de l'entité
        if nouvel_etat == "en_maintenance":
            bien.passer_en_maintenance()
        elif nouvel_etat == "disponible":
            bien.liberer_apres_maintenance()
        elif nouvel_etat == "endommage":
            bien.signalier_endommagement()
        elif nouvel_etat == "archive":
            bien.archiver()
        else:
            raise ValueError("État non supporté")
        self.repo.add(bien)  # Sauvegarde des changements