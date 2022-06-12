from django.contrib import admin
from biblishelf_web.apps.main.models import PathModel
from ._admin import ModelAdmin


@admin.register(PathModel)
class MineTypeModelAdmin(ModelAdmin):
    list_display = (
        'file_modify_time',
        'file_create_time',
        'file_access_time',
        'repo',
        'resource',
        'path',
    )