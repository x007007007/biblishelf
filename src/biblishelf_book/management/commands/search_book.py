from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import RepoModel, ResourceModel
from biblishelf_book.models import BookModel
import os
import fnmatch


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)
        parser.add_argument("-e", "--extname", type=str, nargs='+', default=["pdf", "chm", "epub"])
        parser.add_argument('--ignore_rule', type=str, nargs="+", default=['._*'])

    def handle(self, path=None, extname=None, *args, **options):
        path = os.path.abspath(path)
        ignore_rule = options['ignore_rule']
        self.repo = RepoModel.get_repo_form_path(path)
        self.repo_root_path = RepoModel.get_repo_root_from_path(path)

        print(self.repo)
        print(self.repo_root_path)
        assert isinstance(self.repo, RepoModel)

        for root, dirs, files in os.walk(path):
            for file in files:
                for r in ignore_rule:
                    if fnmatch.fnmatch(file, r):
                        break
                else:
                    if file.split(".").pop() in extname:
                        self.add_book(root, file)

    def add_book(self, root, file):
        file_path = os.path.join(root, file)
        resource, path = self.repo.add_file(
            root_path=self.repo_root_path,
            file_path=file_path
        )
        BookModel.objects.get_or_create(
            defaults=dict(
                name=file,
            ),
            resource=resource,
        )
        print(f"add {file_path} resource: {resource}")
