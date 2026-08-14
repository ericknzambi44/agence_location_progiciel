"""
Use Case : AjusterStockUseCase.

Enregistre un mouvement de stock (entrée, sortie, ajustement)
après validation des règles métier de base et isolation par agence.
"""

from uuid import UUID

from stock.domain.repositories.stock_repository import StockRepository
from stock.domain.repositories.mouvement_stock_repository import MouvementStockRepository
from stock.domain.entities.mouvement_stock import MouvementStock
from stock.domain.value_objects.type_mouvement import TypeMouvement
from stock.domain.exceptions import StockInsuffisantError, ArticleInexistantError


class AjusterStockUseCase:
    """
    Cas d'utilisation : enregistrer un mouvement de stock.

    Attributs :
        stock_repo (StockRepository) : port pour la gestion des niveaux de stock.
        mouvement_repo (MouvementStockRepository) : port pour l'historique des mouvements.
    """

    def __init__(self, stock_repo: StockRepository, mouvement_repo: MouvementStockRepository):
        self.stock_repo = stock_repo
        self.mouvement_repo = mouvement_repo

    def execute(
        self,
        article_id: UUID,
        type_mouvement: str,
        quantite: int,
        motif: str = "",
        user_id: UUID = None,
        agence_id: UUID = None
    ) -> MouvementStock:
        """
        Valide et enregistre un mouvement de stock.

        Args:
            article_id (UUID): Identifiant de l'article concerné.
            type_mouvement (str): Type du mouvement ('entree', 'sortie', etc.)
            quantite (int): Quantité concernée (strictement positive).
            motif (str, optionnel): Motif du mouvement.
            user_id (UUID, optionnel): Utilisateur à l'origine.
            agence_id (UUID, optionnel): Agence pour l'isolation.

        Returns:
            MouvementStock: Entité du mouvement enregistré.

        Raises:
            ValueError: Si données invalides ou stock insuffisant.
        """
        if quantite <= 0:
            raise ValueError("La quantité doit être strictement positive.")

        if agence_id is None:
            raise ValueError("agence_id est requis pour enregistrer un mouvement.")

        # Vérifier que l'article existe et appartient à l'agence
        article = self.stock_repo.get_article(article_id, agence_id=agence_id)
        if article is None:
            raise ArticleInexistantError("Article introuvable ou non autorisé pour votre agence.")

        # Vérifier le stock disponible en cas de sortie
        if type_mouvement == 'sortie':
            disponible = self.stock_repo.get_quantite_disponible(
                article_id=article_id,
                agence_id=agence_id
            )
            if disponible < quantite:
                raise StockInsuffisantError(
                    f"Stock insuffisant : disponible {disponible}, demandé {quantite}."
                )

        # Création de l'entité domaine
        mouvement = MouvementStock(
            article_id=article_id,
            type_mouvement=TypeMouvement(type_mouvement),
            quantite=quantite,
            motif=motif,
            utilisateur_id=user_id,
            agence_id=agence_id,
        )

        # Persistance
        self.mouvement_repo.add(mouvement)

        # Mise à jour du niveau de stock
        if type_mouvement in ['entree', 'retour']:
            self.stock_repo.incrementer_stock(article_id, quantite, agence_id=agence_id)
        elif type_mouvement == 'sortie':
            self.stock_repo.decrementer_stock(article_id, quantite, agence_id=agence_id)

        return mouvement