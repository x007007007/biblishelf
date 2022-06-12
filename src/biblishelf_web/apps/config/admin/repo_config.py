from django.contrib import admin
from biblishelf_web.apps.config.models import RepoConfigModel


@admin.register(RepoConfigModel)
class RepoConfigModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'get_repo_meta',
    )
    list_display = (
        'path',
        'get_repo_meta',
    )

    def action_migrate(self, request, queryset):
        for obj in queryset:
            assert isinstance(obj, RepoConfigModel)
            obj.migrate()

    actions = (
        action_migrate,
    )