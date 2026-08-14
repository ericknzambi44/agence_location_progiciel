from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.management import call_command
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-rbac/', self.admin_view(self.sync_rbac_view), name='sync_rbac'),
        ]
        return custom_urls + urls

    def sync_rbac_view(self, request):
        if request.method == 'POST':
            call_command('sync_rbac', '--create-groups')
            messages.success(request, "RBAC synchronisé.")
            return redirect('admin:index')
        context = dict(
            self.each_context(request),
            title="Synchronisation RBAC",
        )
        return TemplateResponse(request, 'admin/sync_rbac.html', context)