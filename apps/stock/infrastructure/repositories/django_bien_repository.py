from django.core.exceptions import ObjectDoesNotExist
from stock.domain.repositories.bien_repository import BienRepository
from stock.domain.entities.bien import Bien, EtatBien
from stock.infrastructure.models import BienModel
from stock.infrastructure.mappers.bien_mapper import BienMapper
from datetime import date
from uuid import UUID

class DjangoBienRepository(BienRepository):
    def get(self, id: UUID):
        try:
            model = BienModel.objects.get(id=id)
            return BienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def get_by_reference(self, ref):
        try:
            model = BienModel.objects.get(reference=ref.value)
            return BienMapper.to_domain(model)
        except ObjectDoesNotExist:
            return None

    def add(self, bien: Bien):
        model = BienMapper.to_model(bien)
        model.save()
        bien.id = model.id  # synchronisation

    def remove(self, bien: Bien):
        BienModel.objects.filter(id=bien.id).delete()

    def find_by_etat(self, etat: EtatBien):
        models = BienModel.objects.filter(etat=etat.value)
        return [BienMapper.to_domain(m) for m in models]

    def find_disponibles_periode(self, debut: date, fin: date):
        # Règle: bien non réservé sur la période et non en maintenance
        # Sous-requête: biens qui ont une indisponibilité sur la période (réservation ou maintenance)
        # Simplification: on exclut ceux qui sont en maintenance ou réservés dans la plage
        indisponibles = BienModel.objects.filter(
            models.Q(etat='en_maintenance') |
            models.Q(disponibiliteperiode__date_debut__lte=fin, disponibiliteperiode__date_fin__gte=debut, disponibiliteperiode__est_reserve=True)
        ).distinct()
        disponibles = BienModel.objects.exclude(id__in=indisponibles).filter(etat='disponible')
        return [BienMapper.to_domain(m) for m in disponibles]

    def find_all(self):
        return [BienMapper.to_domain(m) for m in BienModel.objects.all()]