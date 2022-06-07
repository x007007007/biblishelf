from django.db import models
from biblishelf_main.models import ExtendResource
from PyPDF2 import PdfFileReader
import json
# Create your models here.
import re


def _book_cover_uploader(*args):
    print(*args)


class Book(ExtendResource):
    publisher = models.ForeignKey("BookPublishing", null=True, blank=True, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=64, null=True, blank=True)
    douban_id = models.CharField(max_length=64, null=True, blank=True)
    set_book = models.ForeignKey('Book', related_name='sub_books', null=True, blank=True, on_delete=models.CASCADE)
    set_type = models.CharField(
        choices=(
            ('series', 'series'),
            ('same', 'same')
        ),
        max_length=8,
        null=True,
        blank=True
    )
    cover = models.ImageField('cover', upload_to=_book_cover_uploader, null=True, blank=True)
    info = models.TextField("info", null=True, blank=True)

    def load_book_info(self, resmap):
        if self.resource.mine_type.startswith("PDF"):
            with open(resmap.get_abs_path(), "rb") as fp:
                try:
                    pdf_obj = PdfFileReader(fp)
                    try:
                        info = pdf_obj.getDocumentInfo()
                        self.info = json.dumps(info, ensure_ascii=False)
                        self.name = info.get("/Title", "").strip("\u0000") or self.name
                    except TypeError:
                        print(pdf_obj.getDocumentInfo())
                    self.page_number = pdf_obj.getNumPages()
                    for page_no in range(0, max(0, min(self.page_number, 5))):
                        page_obj = pdf_obj.getPage(page_no)
                        isbn_rr = re.search("i\s*s\s*b\s*n]", page_obj.extractText(), flags=re.I)
                        if isbn_rr:
                            print("isbn", resmap.get_abs_path())
                            print(isbn_rr.groups())
                    if self.page_number < 0:
                        self.page_number = None
                except PyPDF2.utils.PyPdfError:
                    import traceback
                    traceback.print_exc()
                    self.info = traceback.format_exc()
                except Exception as e:
                    import traceback
                    print("!!!!!!!!!!", e)
                    self.info = traceback.format_exc()
                finally:
                    self.save()


class BookPublishing(models.Model):
    name = models.CharField(max_length=64)

