from biblishelf_book.utils.type.base import BookBaseFileType as BaseFileType
from biblishelf_main.models import ResourceModel
from biblishelf_book.models import Book
from PyPDF2 import PdfFileReader
import PyPDF2.utils


class PdfFileType(BaseFileType):
    @classmethod
    def check_by_description(cls, description):
        if description.strip().startswith("PDF"):
            return True
        return False

    @classmethod
    def get_meta_type(cls):
        return ["application/pdf"]

    def init(self, fp, resource):
        assert isinstance(resource, ResourceModel)
        book = resource.book_set.first()
        assert isinstance(book, Book)
        try:
            pdf_obj = PdfFileReader(fp)
            try:
                info = pdf_obj.getDocumentInfo()
                self._info = json.dumps(info, ensure_ascii=False)
                self._name = info.get("/Title", "").strip("\u0000") or None
                self._author = info.get("/Author", "").strip("\u0000") or None
            except TypeError:
                print(pdf_obj.getDocumentInfo())
            self._page_number = pdf_obj.getNumPages()
            for page_no in range(0, max(0, min(self.page_number, 5))):
                page_obj = pdf_obj.getPage(page_no)
                isbn_rr = re.search("i\s*s\s*b\s*n]", page_obj.extractText(), flags=re.I)
                if isbn_rr:
                    print("isbn", resmap.get_abs_path())
                    print(isbn_rr.groups())
            if self._page_number < 0:
                self._page_number = None
        except PyPDF2.utils.PyPdfError:
            import traceback
            traceback.print_exc()
            self._info = traceback.format_exc()
        except Exception as e:
            import traceback
            self._info = traceback.format_exc()


if __name__ == "__main__":
    PdfFileType()