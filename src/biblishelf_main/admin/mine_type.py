from django.contrib import admin
from biblishelf_main.models import MineTypeModel


@admin.register(MineTypeModel)
class MineTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'mine',
        'detail',
    )