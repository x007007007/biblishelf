from django.contrib import admin
from biblishelf_web.apps.main.models import MimeTypeModel


@admin.register(MimeTypeModel)
class MineTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'mime',
        'detail',
    )