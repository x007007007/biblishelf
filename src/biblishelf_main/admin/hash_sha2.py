from django.contrib import admin
from biblishelf_main.models import HashShaModel


@admin.register(HashShaModel)
class HashShaModelAdmin(admin.ModelAdmin):
    list_display = (
        'frag1',
        'frag2',
        'frag3',
        'frag4',
        'frag5',
        'resource',
    )