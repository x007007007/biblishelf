from django.contrib import admin

from biblishelf_main.models import SubRepoModel


@admin.register(SubRepoModel)
class SubRepoModelAdmin(admin.ModelAdmin):
    list_display = (
        'repo',
        'resource',
    )
