from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import RepoModel, ResourceModel
from biblishelf_book.models import BookModel
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
    help = ''
    read_page_number = 5

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)

    def handle(self, path=None, extname=None, *args, **options):
        repo_root_path = os.path.abspath(path)
        self.repo = RepoModel.get_repo_form_path(repo_root_path)
        self.repo_root_path = RepoModel.get_repo_root_from_path(repo_root_path)
        for resource, file_path in self.repo.iter_resource_abspath(self.repo_root_path):
            if BookModel.objects.filter(resource=resource).exclude(isbn__isnull=True).count() > 0:
                continue
            isbn_list = []
            try:
                for page_num, barcode in self.iter_barcode(file_path):
                    isbn_list.append(barcode.data.decode('utf-8'))
            except:
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

    def set_isbn(self, resource, isbn_num, url):
        BookModel.objects.update_or_create(
            defaults=dict(
                isbn=isbn_num,
                page_number=self.page_number,
            ),
            resource=resource,
        )

    def iter_barcode(self, file_path):
        page_number = 0
        with open(file_path, 'rb') as fp:
            try:
                pdf = PyPDF2.PdfFileReader(fp)
                page_number = pdf.getNumPages()
                self.page_number = page_number
            except:
                traceback.print_exc(
                )
        for i, image in enumerate(convert_from_path(file_path, last_page=self.read_page_number), start=0):  # type: Image
            for bcode in decode_barcode(image):
                yield i, bcode
        if page_number > self.read_page_number:
            for i, image in enumerate(convert_from_path(file_path, first_page=page_number - self.read_page_number, last_page=page_number), start=0):
                for bcode in decode_barcode(image):
                    yield page_number + i, bcode