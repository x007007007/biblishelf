from biblishelf_main.utils.type.base import BaseFileType


class BookBaseFileType(BaseFileType):
    class Meta:
        abstract = True

    _page_number = None
    _info = None
    _cover = None
    _name = None
    _author = None

    def get_name(self):
        return self._name or ""

    def get_pages(self):
        return self._page_number

    def get_author(self):
        return self._author or ""

    def get_cover(self):
        return self._cover or None

    def get_info(self):
        return self._info or None