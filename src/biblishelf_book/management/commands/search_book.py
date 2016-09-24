from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import Repo, ResourceMap, RopeNotExist
from biblishelf_book.models import Book
import os


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, default=os.curdir)
        parser.add_argument("-e", "--extname", type=str, nargs='+', default=["pdf", "chm", "epub"])

    def handle(self, path=None, extname=None, *args, **options):
        path = os.path.abspath(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split(".").pop() in extname:
                    try:
                        resmap = ResourceMap.create_or_update_by_abs_path(
                            path=os.path.join(root, file),
                            ropes=list(Repo.objects.all())
                        )
                        print(resmap)
                        book, _ = Book.objects.get_or_create(
                            resource=resmap.resource,
                        )
                        book.load_book_info(resmap)
                        book.save()
                    except RopeNotExist:
                        raise CommandError("Don't have any rope on the path:{}".format(path))
