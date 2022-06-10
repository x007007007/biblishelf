from django.contrib import admin
from biblishelf_main.models import MimeTypeModel


@admin.register(MimeTypeModel)
class MineTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'mime',
        'detail',
    )