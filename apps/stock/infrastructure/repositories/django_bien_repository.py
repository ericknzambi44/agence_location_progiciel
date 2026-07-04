"""
Repository Django pour les biens.
Toutes les méthodes de lecture filtrent par agence.
"""
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from uuid import UUID
from datetime import date

from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import BienModel
from stock.infrastructure.mappers.bien_mapper import BienMapper
from location.infrastructure.models import ContratModel


class DjangoBienRepository(BienRepository):
    def get(self, id: UUID, agence_id: UUID = None) -> Optional[Bien]:
        try:
            qs = BienModel.objects.filter(id=id)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return BienMapper.to_domain(model)
        except BienModel.DoesNotExist:
            return None

    def get_by_reference(self, reference: str, agence_id: UUID = None) -> Optional[Bien]:
        try:
            qs = BienModel.objects.filter(reference=reference)
            if agence_id is not None:
                qs = qs.filter(agence_id=agence_id)
            model = qs.get()
            return BienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, bien: Bien) -> None:
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
        obj, created = BienModel.objects.update_or_create(id=bien.id, defaults=model_data)
        if created:
            bien.id = obj.id

    def update(self, bien: Bien) -> None:
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

    def find_by_etat(self, etat: EtatBien, agence_id: UUID = None) -> List[Bien]:
        qs = BienModel.objects.filter(etat=etat.value)
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return [BienMapper.to_domain(m) for m in qs]

    def find_disponibles_periode(self, debut: date, fin: date, agence_id: UUID = None) -> List[Bien]:
        qs = BienModel.objects.all()
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)

        # Contrats actifs sur la période
        contrats_actifs = ContratModel.objects.filter(
            statut='actif',
            date_debut__lt=fin,
            date_fin__gt=debut
        )
        if agence_id is not None:
            contrats_actifs = contrats_actifs.filter(agence_id=agence_id)
        contrats_ids = contrats_actifs.values_list('bien_id', flat=True).distinct()

        # Indisponibles : maintenance + contrats actifs
        indisponibles_ids = set(contrats_ids)
        indisponibles_ids.update(qs.filter(etat='en_maintenance').values_list('id', flat=True))

        disponibles = qs.filter(etat='disponible').exclude(id__in=indisponibles_ids)
        return [BienMapper.to_domain(m) for m in disponibles]

    def find_all(self, agence_id: UUID = None) -> List[Bien]:
        if agence_id is None:
            return []  # Sécurité
        models = BienModel.objects.filter(agence_id=agence_id)
        return [BienMapper.to_domain(m) for m in models]