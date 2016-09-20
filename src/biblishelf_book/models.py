from django.db import models
from biblishelf_main.models import ExtendResource
# Create your models here.


def _book_cover_uploader(*args):
    print(*args)


class Book(ExtendResource):
    publisher = models.ForeignKey("BookPublishing", null=True, blank=True)
    page_number = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=64, null=True, blank=True)
    douban_id = models.CharField(max_length=64, null=True, blank=True)
    set_book = models.ForeignKey('Book', related_name='sub_books', null=True, blank=True)
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


class BookPublishing(models.Model):
    name = models.CharField(max_length=64)



