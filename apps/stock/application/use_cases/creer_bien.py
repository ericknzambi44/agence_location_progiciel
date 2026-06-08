from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.value_objects.reference_bien import ReferenceBien
from datetime import date

class CreerBienUseCase:
    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, reference: str, nom: str, description: str = None,
                prix: float = 0.0, date_achat: date = None) -> Bien:
        # Validation via Value Objects et entité
        ref_vo = ReferenceBien(reference)
        bien = Bien(
            reference=ref_vo.value,
            nom=nom,
            description=description,
            prix_unitaire_ht=prix,
            date_achat=date_achat,
            etat=EtatBien.DISPONIBLE
        )
        # Vérifier unicité référence
        existing = self.repo.get_by_reference(ref_vo)
        if existing:
            raise ValueError("Une référence unique est requise.")
        self.repo.add(bien)
        return bien