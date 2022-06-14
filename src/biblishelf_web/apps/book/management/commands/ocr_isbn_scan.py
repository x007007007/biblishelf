from django.core.management.base import BaseCommand, CommandError
from biblishelf_web.apps.main.models import RepoModel, ResourceModel
from biblishelf_web.apps.book.models import BookModel
from django.db.models import Q
import os
from pdf2image import convert_from_path
import PyPDF2
from PIL import Image
from pyzbar.pyzbar import decode as decode_barcode
import cv2
import traceback
import re


class Command(BaseCommand):
    help = ''
    read_page_number = 1

    iter_barcode_failed = 0
    failed = 0
    pypdf_failed = 0

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)

    def handle(self, path=None, extname=None, *args, **options):
        repo_root_path = os.path.abspath(path)
        self.db = RepoModel.load_database_from_path(repo_root_path)

        self.repo = RepoModel.get_repo_form_path(repo_root_path, db=self.db)
        self.repo_root_path = RepoModel.get_repo_root_from_path(repo_root_path)

        for resource, file_path in self.repo.iter_resource_abspath(self.db, self.repo_root_path):
            print(resource, file_path)
            if BookModel.objects.using(self.db).filter(
                    resource=resource
            ).exclude(Q(isbn__isnull=True) | Q(isbn__exact='')).count() > 0:
                print('skip')
                continue
            isbn_list = []
            try:
                for page_num, barcode in self.iter_barcode(file_path):
                    isbn_list.append(barcode.data.decode('utf-8'))
            except KeyboardInterrupt:
                return
            except:
                self.iter_barcode_failed += 1
                self.failed += 1
                traceback.print_exc()
            url = None
            isbn_num = None
            print(isbn_list)
            for cod in isbn_list:
                if len(cod.strip()) == 13 and re.match(r"\d{13}", cod.strip()):
                    isbn_num = cod
                elif cod.startswith("http") or cod.startswith("www"):
                    url = cod
                else:
                    print(cod)
            if len(isbn_list) > 0:
                self.set_isbn(resource, isbn_num, url)
        print(f"""
{self.failed}
{self.iter_barcode_failed}
{self.pypdf_failed}
        """)

    def set_isbn(self, resource, isbn_num, url):
        BookModel.objects.using(self.db).update_or_create(
            defaults=dict(
                isbn=isbn_num,
                page_number=self.page_number,
            ),
            resource=resource,
        )

    def iter_barcode(self, file_path):
        page_number = 0
        if not os.path.exists(file_path):
            print('file not exist')
            return
        with open(file_path, 'rb') as fp:
            try:
                pdf = PyPDF2.PdfFileReader(fp)
                page_number = pdf.getNumPages()
                self.page_number = page_number
            except:
                self.pypdf_failed += 1
                traceback.print_exc()
        for page, image in self.iter_image(file_path, page_number):
            image.save("output.png")
            input()
            continue
            for brcode in decode_barcode(image):
                yield i, brcode

    def iter_image(self, file_path, page_number):
        if page_number <= self.read_page_number * 2:
            for i, image in enumerate(convert_from_path(file_path, last_page=self.read_page_number * 2), start=0):  # type: Image
                yield i, image
        else:
            for i, image in enumerate(convert_from_path(file_path, last_page=self.read_page_number), start=0):
                yield i, image
            end_start = page_number - self.read_page_number + 1
            for i, image in enumerate(convert_from_path(file_path, first_page=end_start), start=end_start):
                yield i, image
