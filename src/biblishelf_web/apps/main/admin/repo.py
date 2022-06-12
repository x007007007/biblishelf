from django.contrib import admin
from biblishelf_web.apps.main.models import RepoModel
from ._admin import ModelAdmin


@admin.register(RepoModel)
class RepoModelAdmin(ModelAdmin):
    list_display = (
        'uuid',
        'is_main',
        'is_portable',
        'media_type',
    )
