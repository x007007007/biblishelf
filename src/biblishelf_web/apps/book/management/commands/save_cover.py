import os.path

from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from biblishelf_web.apps.main.models import RepoModel, ResourceModel
from biblishelf_web.apps.config.models import RepoConfigModel
from biblishelf_web.apps.book.models import BookModel, BookPublishing
import json
import requests


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('db', type=str)

    def handle(self, db, *args, **options):
        m = RepoConfigModel.get_repo_path_map()
        repo_config = m[db]

        for book in BookModel.objects.using(db).exclude(info__isnull=True, douban_id__isnull=True, cover__isnull=True):
            info = json.loads(book.info)
            if publisher_name := info.get('publisher'):
                publish, _ = BookPublishing.objects.using(db).get_or_create(name=publisher_name)
                book.publisher = publish
                book.save(update_fields=('publisher',), using=db)
            if image_url := info.get("image_url"):
                ext_name = image_url.split('.')[-1]
                name = f"{book.isbn}.{ext_name}"
                response = requests.get(image_url)
                if 200 <= response.status_code < 300:
                    book.cover = ContentFile(content=response.content, name=name)
                    book.save(update_fields=('cover',), using=db)
