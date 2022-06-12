import json

from django.db import models, connections, router
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
import os
logger = logging.Logger(__name__)
# Create your models here.

class RepoConfigModel(models.Model):
    path = models.CharField(max_length=254)

    def get_database_config(self) -> dict:
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(self.path, ".bibrepo\index.sqlite3"),
        }

    def is_db_exist(self):
        return os.path.exists()

    def is_repo_exist(self):
        return os.path.exists(self.path, ".bibrepo")

    def get_repo_meta(self):
        path = os.path.join(self.path, ".bibrepo\meta.json")
        if os.path.exists(path):
            with open(path) as fp:
                return json.load(fp)

    def get_database_config_key(self):
        meta = self.get_repo_meta()
        return meta['uuid']

    def migrate(self):
        from django.apps import apps
        connection = connections[self.get_database_config_key()]
        connection.prepare_database()
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
        # Build the manifest of apps and models that are to be synchronized.
        all_models = [
            (
                app_config.label,
                router.get_migratable_models(
                    app_config, connection.alias, include_auto_created=False
                ),
            )
            for app_config in apps.get_app_configs()
            if app_config.models_module is not None
              and app_config.label in ['biblishelf_main']
        ]
        def model_installed(model):
            opts = model._meta
            converter = connection.introspection.identifier_converter
            return not (
                (converter(opts.db_table) in tables)
                or (
                    opts.auto_created
                    and converter(opts.auto_created._meta.db_table) in tables
                )
            )

        manifest = {
            app_name: list(filter(model_installed, model_list))
            for app_name, model_list in all_models
        }
        with connection.schema_editor() as editor:
            for app_name, model_list in manifest.items():
                for model in model_list:
                    # Never install unmanaged models, etc.
                    if not model._meta.can_migrate(connection):
                        continue
                    editor.create_model(model)


@receiver(post_save, sender=RepoConfigModel)
def on_repo_config_save(sender, instance: RepoConfigModel, **kwargs):
    connections.databases[instance.get_database_config_key()] = instance.get_database_config()

