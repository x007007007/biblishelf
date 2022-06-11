from django.contrib import admin

from biblishelf_web.apps.main.models import RepoModel


@admin.register(RepoModel)
class RepoModelAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'is_main',
        'is_portable',
        'media_type',
    )
