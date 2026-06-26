"""
Repository Django pour les biens.
Gère la persistance des entités Bien avec conversion via le mapper.
La vérification de disponibilité intègre les contrats de location actifs.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from typing import Optional, List
from uuid import UUID
from datetime import date

from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import BienModel
from stock.infrastructure.mappers.bien_mapper import BienMapper
from stock.domain.value_objects.prix import PrixHT

# Import du modèle de contrat pour vérifier la disponibilité
from location.infrastructure.models import ContratModel


class DjangoBienRepository(BienRepository):
    """
    Implémentation du repository des biens avec Django ORM.
    """

    def get(self, id: UUID) -> Optional[Bien]:
        try:
            model = BienModel.objects.get(id=id)
            return BienMapper.to_domain(model)
        except BienModel.DoesNotExist:
            return None

    def get_by_reference(self, reference: str) -> Optional[Bien]:
        try:
            model = BienModel.objects.get(reference=reference)
            return BienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, bien: Bien) -> None:
        """
        Ajoute ou met à jour un bien.
        Utilise update_or_create pour éviter les doublons.
        """
        model_data = {
            'id': bien.id,
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description,
            # Extraction du montant et de la devise depuis le Value Object PrixHT
            'prix_unitaire_ht': bien.prix_unitaire_ht.amount,
            'devise': bien.prix_unitaire_ht.currency,
            'date_achat': bien.date_achat,
            'etat': bien.etat.value,
        }
        obj, created = BienModel.objects.update_or_create(id=bien.id, defaults=model_data)
        if created:
            bien.id = obj.id

    def update(self, bien: Bien) -> None:
        """
        Met à jour un bien existant.
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
        BienModel.objects.filter(id=bien.id).update(**model_data)

    def remove(self, bien: Bien) -> None:
        BienModel.objects.filter(id=bien.id).delete()

    def find_by_etat(self, etat: EtatBien) -> List[Bien]:
        models = BienModel.objects.filter(etat=etat.value)
        return [BienMapper.to_domain(m) for m in models]

    def find_disponibles_periode(self, debut: date, fin: date) -> List[Bien]:
        """
        Retourne les biens disponibles sur une période donnée.
        Un bien est indisponible si :
        - Il est en maintenance (etat='en_maintenance')
        - Il a un contrat de location actif qui chevauche la période
        """
        # 1. Récupérer les IDs des biens ayant un contrat actif sur la période
        contrats_actifs = ContratModel.objects.filter(
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        ).values_list('bien_id', flat=True).distinct()

        # 2. Biens indisponibles (maintenance + contrats actifs)
        indisponibles_ids = set(contrats_actifs)
        indisponibles_ids.update(
            BienModel.objects.filter(etat='en_maintenance').values_list('id', flat=True)
        )

        # 3. Biens disponibles (état disponible et pas dans la liste des indisponibles)
        disponibles = BienModel.objects.filter(
            etat='disponible'
        ).exclude(id__in=indisponibles_ids)

        return [BienMapper.to_domain(m) for m in disponibles]

    def find_all(self) -> List[Bien]:
        models = BienModel.objects.all()
        return [BienMapper.to_domain(m) for m in models]