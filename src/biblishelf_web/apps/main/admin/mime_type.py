from django.contrib import admin
from biblishelf_web.apps.main.models import MimeTypeModel
from ._admin import ModelAdmin


@admin.register(MimeTypeModel)
class MineTypeModelAdmin(ModelAdmin):
    list_display = (
        'mime',
        'detail',
    )