from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from typing import Optional, List
from uuid import UUID
from datetime import date
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import BienModel
from stock.infrastructure.mappers.bien_mapper import BienMapper

class DjangoBienRepository(BienRepository):
    def get(self, id: UUID) -> Optional[Bien]:
      try:
        # Convertir l'UUID en chaîne pour éviter les problèmes de type
        model = BienModel.objects.get(id=id)
        return BienMapper.to_domain(model)
      except BienModel.DoesNotExist:
        # Essayer avec une conversion en chaîne
        try:
            model = BienModel.objects.get(id=str(id))
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
        model_data = {
            'id': bien.id,
            'reference': bien.reference,
            'nom': bien.nom,
            'description': bien.description,
            'prix_unitaire_ht': bien.prix_unitaire_ht,
            'date_achat': bien.date_achat,
            'etat': bien.etat.value,
        }
        obj, created = BienModel.objects.update_or_create(id=bien.id, defaults=model_data)
        if created:
            bien.id = obj.id

    def remove(self, bien: Bien) -> None:
        BienModel.objects.filter(id=bien.id).delete()

    def find_by_etat(self, etat: EtatBien) -> List[Bien]:
        models = BienModel.objects.filter(etat=etat.value)
        return [BienMapper.to_domain(m) for m in models]

    def find_disponibles_periode(self, debut: date, fin: date) -> List[Bien]:
        indisponibles = BienModel.objects.filter(
            Q(etat='en_maintenance') |
            Q(disponibiliteperiodemodel__date_debut__lte=fin,
              disponibiliteperiodemodel__date_fin__gte=debut,
              disponibiliteperiodemodel__est_reserve=True)
        ).distinct()
        disponibles = BienModel.objects.exclude(id__in=indisponibles).filter(etat='disponible')
        return [BienMapper.to_domain(m) for m in disponibles]

    def find_all(self) -> List[Bien]:
        models = BienModel.objects.all()
        return [BienMapper.to_domain(m) for m in models]