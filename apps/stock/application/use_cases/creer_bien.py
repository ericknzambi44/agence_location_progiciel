"""
Use case pour créer un nouveau bien.
Valide les données, vérifie l'unicité de la référence et persiste le bien.
"""
from datetime import date
from decimal import Decimal

from stock.domain.entities.bien import Bien, EtatBien
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.value_objects.reference_bien import ReferenceBien
from stock.domain.value_objects.prix import PrixHT


class CreerBienUseCase:
    """
    Use case de création d'un bien.

    Args:
        repo (BienRepository): Repository pour la persistance des biens.
    """

    def __init__(self, repo: BienRepository):
        self.repo = repo

    def execute(self, reference: str, nom: str, description: str = None,
                prix: float = 0.0, currency: str = "USD", date_achat: date = None) -> Bien:
        """
        Exécute la création d'un bien.

        Args:
            reference (str): Référence unique du bien.
            nom (str): Nom du bien.
            description (str, optional): Description. Défaut None.
            prix (float): Prix unitaire HT par jour.
            currency (str): Devise (ISO 4217). Défaut "USD".
            date_achat (date, optional): Date d'achat. Défaut None.

        Returns:
            Bien: L'entité bien créée.

        Raises:
            ValueError: Si la référence existe déjà ou si les données sont invalides.
        """
        # 1. Validation et création des Value Objects
        ref_vo = ReferenceBien(reference)
        prix_vo = PrixHT(amount=Decimal(str(prix)), currency=currency)

        # 2. Vérification de l'unicité de la référence
        existing = self.repo.get_by_reference(ref_vo)
        if existing:
            raise ValueError("Une référence unique est requise.")

        # 3. Construction de l'entité
        bien = Bien(
            reference=ref_vo.value,
            nom=nom,
            description=description,
            prix_unitaire_ht=prix_vo,
            date_achat=date_achat,
            etat=EtatBien.DISPONIBLE
        )

        # 4. Persistance
        self.repo.add(bien)

        return bien