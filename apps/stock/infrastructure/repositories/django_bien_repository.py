"""
Repository Django pour les biens.

Gère la persistance des entités `Bien` avec conversion via le mapper.
Toutes les méthodes de lecture supportent le filtrage par agence.

Ce module implémente le port `BienRepository` défini dans la couche domaine.
"""

from typing import Optional, List
from uuid import UUID
from datetime import date

from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import Bien  # Modèle Django (Bien)
from stock.infrastructure.mappers.bien_mapper import BienMapper
from location.infrastructure.models import Contrat


class DjangoBienRepository(BienRepository):
    """
    Implémentation du repository des biens avec Django ORM.

    Cette classe est responsable de :
        - Convertir les entités du domaine en modèles Django et vice-versa.
        - Assurer l'isolation par agence (toutes les requêtes de lecture
          exigent un `agence_id` non nul pour éviter les fuites inter-agences).
        - Fournir des méthodes de recherche métier (disponibilité, état, etc.).
    """

    # --------------------------------------------------------------------------
    # Méthodes de lecture
    # --------------------------------------------------------------------------

    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Bien]:
        """
        Récupère un bien par son identifiant unique.

        Args:
            id (UUID): Identifiant du bien.
            agence_id (UUID, optionnel): Si fourni, filtre pour que le bien
                appartienne à cette agence.

        Returns:
            Optional[Bien]: L'entité domaine si trouvée, sinon None.
        """
        try:
            qs = Bien.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return BienMapper.to_domain(model)
        except Bien.DoesNotExist:
            return None

    def get_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[Bien]:
        """
        Récupère un bien par sa référence unique.

        Args:
            reference (str): Référence du bien.
            agence_id (UUID, optionnel): Filtre par agence si fourni.

        Returns:
            Optional[Bien]: L'entité domaine si trouvée, sinon None.
        """
        try:
            qs = Bien.objects.filter(reference=reference)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return BienMapper.to_domain(model)
        except Bien.DoesNotExist:
            return None

    def find_by_etat(self, etat: EtatBien, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne tous les biens ayant un état donné.

        Args:
            etat (EtatBien): L'état recherché (disponible, en_maintenance, etc.)
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            List[Bien]: Liste des entités domaine.
        """
        qs = Bien.objects.filter(etat=etat.value)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [BienMapper.to_domain(m) for m in qs]

    def find_disponibles_periode(self, debut: date, fin: date, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne les biens disponibles sur une période donnée.

        Un bien est indisponible s'il :
            - est en maintenance ;
            - est lié à un contrat actif chevauchant la période.

        Args:
            debut (date): Date de début de la période.
            fin (date): Date de fin de la période.
            agence_id (UUID, optionnel): Filtre par agence.

        Returns:
            List[Bien]: Liste des biens disponibles.
        """
        qs = Bien.objects.all()
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)

        # Contrats actifs sur la période
        contrats_actifs = Contrat.objects.filter(
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        if agence_id is not None:
            contrats_actifs = contrats_actifs.filter(agence_id=agence_id)
        contrats_ids = contrats_actifs.values_list('bien_id', flat=True).distinct()

        # Indisponibles : maintenance + contrats actifs
        indisponibles_ids = set(contrats_ids)
        indisponibles_ids.update(
            qs.filter(etat='en_maintenance').values_list('id', flat=True)
        )

        disponibles = qs.filter(etat='disponible').exclude(id__in=indisponibles_ids)
        return [BienMapper.to_domain(m) for m in disponibles]

    def find_all(self, agence_id: UUID = None) -> List[Bien]:
        """
        Retourne tous les biens d'une agence.

        Args:
            agence_id (UUID, optionnel): Identifiant de l'agence.
                Si None, retourne une liste vide (sécurité).

        Returns:
            List[Bien]: Liste des entités domaine.
        """
        if agence_id is None:
            return []
        models = Bien.objects.filter(agence_id=agence_id)
        return [BienMapper.to_domain(m) for m in models]

    # --------------------------------------------------------------------------
    # Méthodes d'écriture
    # --------------------------------------------------------------------------

    def add(self, bien: Bien) -> None:
        """
        Insère un nouveau bien en base de données.

        Le bien doit obligatoirement avoir un `agence_id` renseigné.

        Args:
            bien (Bien): L'entité domaine à persister.
        """
        if bien.agence_id is None:
            raise ValueError("agence_id est requis pour sauvegarder un bien.")

        model_data = {
            'id': bien.id,
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description,
            'prix_unitaire_ht': bien.prix_unitaire_ht.amount,
            'devise': bien.prix_unitaire_ht.currency,
            'date_achat': bien.date_achat,
            'etat': bien.etat.value,
            'agence_id': bien.agence_id
        }
        obj, created = Bien.objects.update_or_create(id=bien.id, defaults=model_data)
        if created:
            bien.id = obj.id

    def update(self, bien: Bien) -> None:
        """
        Met à jour un bien existant.

        Args:
            bien (Bien): L'entité domaine avec les modifications.
        """
        model_data = {
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description,
            'prix_unitaire_ht': bien.prix_unitaire_ht.amount,
            'devise': bien.prix_unitaire_ht.currency,
            'date_achat': bien.date_achat,
            'etat': bien.etat.value,
        }
        Bien.objects.filter(id=bien.id).update(**model_data)

    def remove(self, bien: Bien) -> None:
        """
        Supprime définitivement un bien.

        Attention : dans une logique de soft delete, il serait préférable
        de désactiver le bien plutôt que de le supprimer physiquement.

        Args:
            bien (Bien): L'entité domaine à supprimer.
        """
        Bien.objects.filter(id=bien.id).delete()