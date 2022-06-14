from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from biblishelf_web.apps.main.models import (
    RepoModel,
    ResourceModel,
)
import os
import uuid


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)
        parser.add_argument('--rehash', action='store_true')
        parser.add_argument('--name', type=str)


    def handle(self, path=None, rehash=False, name=None, *args, **options):
        path = os.path.abspath(path)
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

