from biblishelf_core.hook import ScanHooker
from biblishelf_core.shortcut import get_or_create, create_or_update
from PyPDF2 import PdfFileReader
from .models import Book, CatalogItem, BookAuthor, PdfBook, PdfBookProducer, PdfBookCreator
import PyPDF2.utils
import re
import traceback
import datetime


class PdfScanHooker(ScanHooker):
    pdf_timestr_re = re.compile(r"D:(\d{14}[+\-]\d\d)'(\d\d)'")

    @staticmethod
    def hooker_mime_type(mime_type, mime):
        if mime_type in ['application/pdf']:
            return True
        else:
            return False

    def pdf_strptime(self, str):
        time_str_rr = self.pdf_timestr_re.match(str)
        if time_str_rr:
            time_str = "".join(time_str_rr.groups())
            return datetime.datetime.strptime(
                time_str, '%Y%m%d%H%M%S%z'
            )
        return None

    def get_fp(self, fp):
        session = self.repo.Session()
        try:
            pdf_obj = PdfFileReader(fp)
            default = {}
            book_default = {}
            info = pdf_obj.getDocumentInfo()
            if '/Creator' in info and info['/Creator'].strip():
                default["pdf_book_producer"], _= get_or_create(session, PdfBookProducer, name=info['/Creator'].strip())
            if '/Producer' in info and info['/Producer'].strip():
                default["pdf_book_creator"], _= get_or_create(session, PdfBookCreator, name=info['/Producer'].strip())
            if '/CreationDate' in info:
                default["create_time"] = self.pdf_strptime(info["/CreationDate"].strip())
            if '/ModDate' in info:
                default["modify_time"] = self.pdf_strptime(info["/ModDate"].strip())
            book_default['page'] = pdf_obj.getNumPages()
            book, is_update= create_or_update(session, Book, book_default, resource_id=self.resource.id)
            book_pdf , is_update = create_or_update(session, PdfBook, default=default, book=book)
            session.commit()

        except PyPDF2.utils.PyPdfError:
            traceback.print_exc()
            self._info = traceback.format_exc()
            session.rollback()
        except Exception as e:
            traceback.print_exc()
            self._info = traceback.format_exc()
            session.rollback()
