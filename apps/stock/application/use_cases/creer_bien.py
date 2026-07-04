"""
Use case pour créer un nouveau bien.
Valide les données, vérifie l'unicité de la référence,
assigne l'agence_id et persiste le bien.
"""
from datetime import date
from decimal import Decimal
from uuid import UUID

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
                prix: float = 0.0, currency: str = "USD", date_achat: date = None,
                agence_id: UUID = None) -> Bien:
        """
        Exécute la création d'un bien.

        Args:
            reference (str): Référence unique du bien.
            nom (str): Nom du bien.
            description (str, optional): Description. Défaut None.
            prix (float): Prix unitaire HT par jour.
            currency (str): Devise (ISO 4217). Défaut "USD".
            date_achat (date, optional): Date d'achat. Défaut None.
            agence_id (UUID): Identifiant de l'agence propriétaire. Obligatoire.

        Returns:
            Bien: L'entité bien créée.

        Raises:
            ValueError: Si la référence existe déjà, si les données sont invalides,
                        ou si agence_id est manquant.
        """
        if agence_id is None:
            raise ValueError("agence_id est requis pour créer un bien.")

        # 1. Validation et création des Value Objects
        ref_vo = ReferenceBien(reference)
        prix_vo = PrixHT(amount=Decimal(str(prix)), currency=currency)

        # 2. Vérification de l'unicité de la référence (dans l'agence)
        existing = self.repo.get_by_reference(ref_vo, agence_id=agence_id)
        if existing:
            raise ValueError("Une référence unique est requise dans cette agence.")

        # 3. Construction de l'entité
        bien = Bien(
            reference=ref_vo.value,
            nom=nom,
            description=description,
            prix_unitaire_ht=prix_vo,
            date_achat=date_achat,
            etat=EtatBien.DISPONIBLE,
            agence_id=agence_id
        )

        # 4. Persistance
        self.repo.add(bien)

        return bien