from django.core.management.base import BaseCommand, CommandError
from biblishelf_web.apps.main.models import RepoModel, ResourceModel
from biblishelf_web.apps.plugins.book.models import BookModel
import PyPDF2
import traceback
import os
from pdf2image import convert_from_path
import PyPDF2
from PIL import Image
from pyzbar.pyzbar import decode as decode_barcode
import traceback
import re


class Command(BaseCommand):
    help = '删除掉repo中不存在的文件路径记录'
    read_page_number = 5

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)

    def handle(self, path=None, extname=None, *args, **options):
        repo_root_path = os.path.abspath(path)
        self.db = RepoModel.load_database_from_path(repo_root_path)

        self.repo = RepoModel.get_repo_form_path(repo_root_path, db=self.db)
        self.repo_root_path = RepoModel.get_repo_root_from_path(repo_root_path)

        for resource, file_path in self.repo.iter_resource_abspath(self.db, self.repo_root_path):
            for path in resource.pathmodel_set.using(self.db).all():
                file_path = os.path.join(self.repo_root_path, path.path)
                if not os.path.exists(file_path):
                    path.delete(using=self.db)
