"""
Repository Django pour les statistiques.
Toutes les méthodes filtrent par agence.
"""
from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import date
from uuid import UUID
from django.db.models import Sum, Count, Avg, Q, F, StdDev, Min, Max
from django.db.models.functions import TruncMonth, TruncDay, TruncYear

from location.infrastructure.models import ContratModel
from stock.infrastructure.models import BienModel
from maintenance.infrastructure.models import InterventionModel, InterventionPieceModel, PieceDetacheeModel
from rh.infrastructure.models import EmployeModel

from statistiques.domain.repositories.statistiques_repository import StatistiquesRepository
from statistiques.domain.value_objects.periode import Periode, UnitePeriode


class DjangoStatistiquesRepository(StatistiquesRepository):
    def _trunc_periode(self, periode: Periode):
        if periode.unite == UnitePeriode.JOUR:
            return TruncDay('date_debut')
        elif periode.unite == UnitePeriode.MOIS:
            return TruncMonth('date_debut')
        else:
            return TruncYear('date_debut')

    # --- Revenus ---
    def get_revenus_par_periode(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='termine'
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.annotate(
            periode_label=self._trunc_periode(periode)
        ).values('periode_label').annotate(
            total=Sum('montant_total')
        ).order_by('periode_label')
        return list(qs)

    def get_revenus_par_bien(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='termine'
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('bien_id').annotate(
            total=Sum('montant_total'),
            nb_contrats=Count('id')
        ).order_by('-total')
        result = []
        for item in qs:
            bien = BienModel.objects.filter(id=item['bien_id']).first()
            result.append({
                'bien_id': str(item['bien_id']),
                'nom': bien.nom if bien else 'Inconnu',
                'total_revenus': item['total'],
                'nb_contrats': item['nb_contrats']
            })
        return result

    def get_revenus_par_client(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='termine'
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('client_id').annotate(
            total=Sum('montant_total'),
            nb_contrats=Count('id')
        ).order_by('-total')
        result = []
        for item in qs:
            result.append({
                'client_id': str(item['client_id']),
                'total_depense': item['total'],
                'nb_contrats': item['nb_contrats']
            })
        return result

    # --- Contrats ---
    def get_nombre_contrats_par_periode(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.annotate(
            periode_label=self._trunc_periode(periode)
        ).values('periode_label').annotate(
            total=Count('id')
        ).order_by('periode_label')
        return list(qs)

    def get_nombre_contrats_par_statut(self, periode: Periode, agence_id: UUID = None) -> Dict[str, int]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('statut').annotate(total=Count('id'))
        result = {'actif': 0, 'termine': 0, 'annule': 0}
        for item in qs:
            result[item['statut']] = item['total']
        return result

    # --- Taux d'occupation ---
    def get_taux_occupation_global(self, periode: Periode, agence_id: UUID = None) -> float:
        qs_biens = BienModel.objects.filter(etat__in=['disponible', 'en_maintenance'])
        if agence_id is not None:
            qs_biens = qs_biens.filter(agence_id=agence_id)
        total_biens = qs_biens.count()

        qs_contrats = ContratModel.objects.filter(
            statut='actif',
            date_debut__lte=periode.fin,
            date_fin__gte=periode.debut
        )
        if agence_id is not None:
            qs_contrats = qs_contrats.filter(agence_id=agence_id)
        nb_contrats = qs_contrats.count()

        if total_biens == 0:
            return 0.0
        return nb_contrats / total_biens

    def get_taux_occupation_par_bien(self, bien_id: UUID, periode: Periode, agence_id: UUID = None) -> float:
        nb_jours = (periode.fin - periode.debut).days + 1
        qs = ContratModel.objects.filter(
            bien_id=bien_id,
            statut='actif',
            date_debut__lte=periode.fin,
            date_fin__gte=periode.debut
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        total_jours_occupe = sum((min(c.date_fin, periode.fin) - max(c.date_debut, periode.debut)).days + 1 for c in qs)
        return total_jours_occupe / nb_jours if nb_jours > 0 else 0

    # --- Biens populaires ---
    def get_biens_les_plus_loues(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('bien_id').annotate(
            total=Count('id'),
            revenus=Sum('montant_total')
        ).order_by('-total')[:limite]
        result = []
        for item in qs:
            bien = BienModel.objects.filter(id=item['bien_id']).first()
            result.append({
                'bien_id': str(item['bien_id']),
                'nom': bien.nom if bien else 'Inconnu',
                'reference': bien.reference if bien else '',
                'nb_contrats': item['total'],
                'revenus': item['revenus'] or Decimal(0)
            })
        return result

    # --- Pièces populaires ---
    def get_pieces_les_plus_utilisees(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        interventions_qs = InterventionModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='terminee'
        )
        if agence_id is not None:
            interventions_qs = interventions_qs.filter(agence_id=agence_id)

        qs = InterventionPieceModel.objects.filter(
            intervention__in=interventions_qs
        ).values('piece_id').annotate(
            total_quantite=Sum('quantite'),
            total_cout=Sum(F('quantite') * F('piece__prix_unitaire'))
        ).order_by('-total_quantite')[:limite]
        result = []
        for item in qs:
            piece = PieceDetacheeModel.objects.filter(id=item['piece_id']).first()
            result.append({
                'piece_id': str(item['piece_id']),
                'nom': piece.nom if piece else 'Inconnu',
                'reference': piece.reference if piece else '',
                'quantite_totale': item['total_quantite'],
                'cout_total': item['total_cout'] or Decimal(0)
            })
        return result

    # --- Interventions par technicien ---
    def get_interventions_par_technicien(self, periode: Periode, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = InterventionModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='terminee'
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('technicien_id').annotate(
            nb=Count('id'),
            cout_total=Sum('cout_total'),
            duree_moyenne=Avg(F('date_fin') - F('date_debut'))
        ).order_by('-nb')
        result = []
        for item in qs:
            technicien = None
            if item['technicien_id']:
                technicien = EmployeModel.objects.filter(id=item['technicien_id']).first()
                nom = f"{technicien.prenom} {technicien.nom}" if technicien else 'Inconnu'
            else:
                nom = 'Non assigné'
            duree_moyenne = item['duree_moyenne']
            result.append({
                'technicien_id': str(item['technicien_id']) if item['technicien_id'] else None,
                'nom': nom,
                'nb_interventions': item['nb'],
                'cout_total': item['cout_total'] or Decimal(0),
                'duree_moyenne': duree_moyenne.total_seconds() / 3600 if duree_moyenne else 0
            })
        return result

    def get_statistiques_interventions(self, periode: Periode, agence_id: UUID = None) -> Dict[str, Any]:
        qs = InterventionModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin,
            statut='terminee'
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.aggregate(
            nb_total=Count('id'),
            cout_moyen=Avg('cout_total'),
            duree_moyenne=Avg(F('date_fin') - F('date_debut')),
            duree_min=Min(F('date_fin') - F('date_debut')),
            duree_max=Max(F('date_fin') - F('date_debut')),
            stddev=StdDev(F('date_fin') - F('date_debut'))
        )
        duree_moyenne = qs['duree_moyenne']
        duree_min = qs['duree_min']
        duree_max = qs['duree_max']
        stddev = qs['stddev']
        return {
            'nb_total': qs['nb_total'] or 0,
            'cout_moyen': qs['cout_moyen'] or Decimal(0),
            'duree_moyenne_heures': duree_moyenne.total_seconds() / 3600 if duree_moyenne else 0,
            'duree_min_heures': duree_min.total_seconds() / 3600 if duree_min else 0,
            'duree_max_heures': duree_max.total_seconds() / 3600 if duree_max else 0,
            'ecart_type_heures': stddev.total_seconds() / 3600 if stddev else 0,
        }

    # --- Clients ---
    def get_nombre_clients_actifs(self, periode: Periode, agence_id: UUID = None) -> int:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        return qs.values('client_id').distinct().count()

    def get_clients_plus_actifs(self, periode: Periode, limite: int = 5, agence_id: UUID = None) -> List[Dict[str, Any]]:
        qs = ContratModel.objects.filter(
            date_debut__gte=periode.debut,
            date_debut__lte=periode.fin
        )
        if agence_id is not None:
            qs = qs.filter(agence_id=agence_id)
        qs = qs.values('client_id').annotate(
            nb_contrats=Count('id'),
            total_depense=Sum('montant_total')
        ).order_by('-nb_contrats')[:limite]
        result = []
        for item in qs:
            result.append({
                'client_id': str(item['client_id']),
                'nb_contrats': item['nb_contrats'],
                'total_depense': item['total_depense'] or Decimal(0)
            })
        return result