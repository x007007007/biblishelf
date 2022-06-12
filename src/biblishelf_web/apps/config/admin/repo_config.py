from django.contrib import admin
from biblishelf_web.apps.config.models import RepoConfigModel


@admin.register(RepoConfigModel)
class RepoConfigModelAdmin(admin.ModelAdmin):
    list_display = (
        'path',
    )