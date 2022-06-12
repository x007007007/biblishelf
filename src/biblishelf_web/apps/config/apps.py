import traceback

from django.apps import AppConfig
from django.db import connections


class BiblishelfConfigConfig(AppConfig):

    name = 'biblishelf_web.apps.config'
    label = 'biblishelf_config'

    def ready(self):
        from .models import RepoConfigModel  # or...
        RepoConfigModel = self.get_model('RepoConfigModel')
        for config in RepoConfigModel.objects.all():
            try:
                connections.databases[config.get_database_config_key()] = config.get_database_config()
                print(f"config db: {config.get_database_config_key()}")
            except:
                traceback.print_exc()