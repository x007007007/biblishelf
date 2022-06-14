from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from biblishelf_web.apps.main.models import (
    RepoModel,
    ResourceModel,
)
import os
import uuid
import importlib


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)
        parser.add_argument('--rehash', action='store_true')
        parser.add_argument('--name', type=str)
        parser.add_argument('--add-plugin', action='append', type=str)
        parser.add_argument('--del-plugin', action='append', type=str)

    def plugin_check(self, plugins):
        for p in plugins:
            try:
                plugin_app = importlib.import_module('apps', f'biblishelf_web.apps.plugins.{p}')
            except ImportError:
                raise CommandError(f"unknown plugin '{p}'")

    def handle(self, path=None, rehash=False, name=None, add_plugin=None, del_plugin=None, *args, **options):
        path = os.path.abspath(path)
        if isinstance(add_plugin, str):
            add_plugin = [add_plugin]
        if isinstance(del_plugin, str):
            del_plugin = [del_plugin]
        if add_plugin or del_plugin:
            plugin_list = []
            if add_plugin:
                plugin_list.extend(add_plugin)
            if del_plugin:
                plugin_list.extend(del_plugin)
            self.plugin_check(plugin_list)

        self.db = RepoModel.load_database_from_path(path)
        repo_root = RepoModel.get_repo_root_from_path(path)
        meta = RepoModel.get_repo_meta_form_root(repo_root)
        repo = RepoModel.get_repo_form_path(repo_root, self.db)

        if rehash:
            new_uuid = uuid.uuid4().hex
            print(f"rehash db: {meta['uuid']} {repo.uuid}-> {new_uuid}")
            with transaction.atomic(using=self.db):
                repo.uuid = new_uuid
                repo.save(update_fields=('uuid',), using=self.db)
                RepoModel.save_repo_meta({
                    'uuid': new_uuid,
                }, repo_root)
        if name:
            with transaction.atomic(using=self.db):
                repo.name = name
                repo.save(update_fields=('uuid',), using=self.db)
                RepoModel.save_repo_meta({
                    'name': name,
                }, repo_root)
        meta = RepoModel.get_repo_meta_form_root(root=repo_root)
        plugins = meta.get('plugin', [])
        old_plugin = tuple(plugins)
        if add_plugin:
            for p in add_plugin:
                if p not in plugins:
                    plugins.append(p)
        if del_plugin:
            for p in plugins:
                plugins.remove(p)
        if old_plugin != tuple(plugins):
            RepoModel.save_repo_meta({
                'plugin': plugins,
            }, repo_root)
