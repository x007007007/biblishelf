from django.contrib import admin
from biblishelf_web.apps.main.models import SubRepoModel
from ._admin import ModelAdmin


@admin.register(SubRepoModel)
class SubRepoModelAdmin(ModelAdmin):
    list_display = (
        'repo',
        'resource',
    )
