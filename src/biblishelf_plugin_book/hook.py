from biblishelf_core.hook import ScanHooker
from PyPDF2 import PdfFileReader
from .models import Book
import PyPDF2.utils
import re

class PdfScanHooker(ScanHooker):

    def get_fp(self, fp):
        assert isinstance(fp, open)
        try:
            pdf_obj = PdfFileReader(fp)
            try:
                info = pdf_obj.getDocumentInfo()
                print(info)
            except TypeError:
                pass
            page_number = pdf_obj.getNumPages()

        except PyPDF2.utils.PyPdfError:
            import traceback
            traceback.print_exc()
            self._info = traceback.format_exc()
        except Exception as e:
            import traceback
            self._info = traceback.format_exc()