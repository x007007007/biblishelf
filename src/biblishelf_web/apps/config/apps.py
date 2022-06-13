import traceback

from django.apps import AppConfig
from django.db import connections


class BiblishelfConfigConfig(AppConfig):

    name = 'biblishelf_web.apps.config'
    label = 'biblishelf_config'

    def ready(self):
        from .models import RepoConfigModel  # or...
        RepoConfigModel = self.get_model('RepoConfigModel')
        for config in RepoConfigModel.objects.only('path').all():
            if k := config.update_database_map():
                print(f"config db: {k}")
