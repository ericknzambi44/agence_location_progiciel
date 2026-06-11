from django.contrib import admin
from .infrastructure.models import EmployeModel, PointageModel, EvaluationModel, RoleModel

@admin.register(EmployeModel)
class EmployeModelAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'email', 'est_actif')
    search_fields = ('matricule', 'nom', 'prenom', 'email')
    list_filter = ('est_actif',)

@admin.register(PointageModel)
class PointageModelAdmin(admin.ModelAdmin):
    list_display = ('employe', 'horodatage', 'type')
    list_filter = ('type',)

@admin.register(EvaluationModel)
class EvaluationModelAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_evaluation', 'note')
    list_filter = ('date_evaluation',)

@admin.register(RoleModel)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ('nom',)