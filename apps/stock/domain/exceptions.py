"""
Exceptions métier du module Stock.
"""


class StockDomainError(Exception):
    """Erreur de base du domaine stock."""


class ArticleInexistantError(StockDomainError):
    """L'article demandé n'existe pas ou n'appartient pas à l'agence."""


class StockInsuffisantError(StockDomainError):
    """Le stock disponible est inférieur à la quantité demandée."""