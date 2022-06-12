import json

from django.db import models, router
import os
import time
import datetime
import pytz
from django.db import connections


class RepoModel(models.Model):
    name = models.CharField(null=True, blank=True, max_length=254)
    uuid = models.UUIDField(unique=True, null=False)
    is_main = models.BooleanField(default=False)
    is_portable = models.BooleanField(default=True)
    media_type = models.CharField(
        choices=(
            ("disc", "disc"),
            ("ssd", "ssd"),
            ("usb-disc", "usb-disc"),
            ("cd", "cd"),
            ("usb-ssd", 'usb-ssd'),
            ("tf/sd", "tf-sd"),
            ("samba", "samba"),
            ("cloud", "cloud")
        ),
        max_length=32
    )

    @classmethod
    def load_database_from_path(cls, curp):
        root_path = cls.get_repo_root_from_path(curp)
        repo_meta_path = os.path.join(root_path, '.bibrepo/meta.json')
        with open(repo_meta_path) as fp:
            meta = json.load(fp)
        m_uuid = meta['uuid']
        connections.databases[m_uuid] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(root_path, ".bibrepo\index.sqlite3"),
        }
        cls.migrate(m_uuid)
        return m_uuid

    @classmethod
    def migrate(cls, database):
        from django.apps import apps
        connection = connections[database]
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
              and app_config.label in ['biblishelf_main', 'biblishelf_book']
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

    @classmethod
    def get_repo_root_from_path(cls, curp):
        repo_meta_path = os.path.join(curp, '.bibrepo/meta.json')
        if os.path.exists(repo_meta_path):
            return curp
        if (parent_path := os.path.dirname(curp)) != curp:
            return cls.get_repo_root_from_path(parent_path)

    @classmethod
    def get_repo_form_path(cls, curp):
        repo_root = cls.get_repo_root_from_path(curp)
        repo_meta_path = os.path.join(repo_root, '.bibrepo/meta.json')
        if os.path.exists(repo_meta_path):
            with open(repo_meta_path) as fp:
                meta = json.load(fp)
                return cls.objects.get_or_create(
                    defaults=dict(
                        name=meta['repo'],
                    ),
                    uuid=meta['uuid'],
                )[0]

    def add_file(self, db, root_path, file_path):
        from .resource import ResourceModel
        from .path import PathModel
        file_path = os.path.abspath(file_path)
        root_path = os.path.abspath(root_path)
        resource, _ = ResourceModel.get_or_create_from_abs_path(file_path)
        path, _ = PathModel.objects.using(db).get_or_create(
            defaults=dict(
                file_modify_time=datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=pytz.utc),
                file_create_time=datetime.datetime.fromtimestamp(os.path.getctime(file_path), tz=pytz.utc),
                file_access_time=datetime.datetime.fromtimestamp(os.path.getatime(file_path), tz=pytz.utc),
            ),
            repo=self,
            resource=resource,
            path=file_path[len(root_path):].lstrip('/')
        )
        return resource, path

    def iter_resource_abspath(self, db, base_root):
        assert os.path.exists(os.path.join(base_root, '.bibrepo/meta.json'))
        from .resource import ResourceModel
        from .path import PathModel
        for resource in ResourceModel.objects.using(db).filter(pathmodel__repo=self):
            res = resource.pathmodel_set.order_by('-file_access_time').first()
            assert isinstance(res, PathModel)
            yield resource, os.path.join(base_root, res.path)


