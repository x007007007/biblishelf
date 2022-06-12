from django.contrib import admin
from biblishelf_web.apps.main.models import HashShaModel
from ._admin import ModelAdmin


@admin.register(HashShaModel)
class HashShaModelAdmin(ModelAdmin):
    list_display = (
        'frag1',
        'frag2',
        'frag3',
        'frag4',
        'frag5',
        'resource',
    )