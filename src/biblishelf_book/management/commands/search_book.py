from django.core.management.base import BaseCommand, CommandError
from watchdog.observers import Observer
from biblishelf_main.models import ConfigWatchArea, Repo, ResourceMap, Resource
from biblishelf_book.models import Book
from pathinfo import mount
import os
import hashlib
pi = mount.PathInfo()


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for root, dirs, files in os.walk(wa.path):
            for file in [file for file in files if file.endswith(".pdf")]:
                path = os.path.join(root, file)
                vol, relpath = pi.get_path(path)
                repo, _ = Repo.objects.get_or_create(uuid=vol)
                try:
                    if ResourceMap.objects.filter(repo=repo, path=relpath).count() == 0:
                        sha1 = hashlib.sha1()
                        with open(path, 'rb') as fp:
                            length = 0
                            while True:
                                res = fp.read(1024 * 512)
                                if len(res) == 0: break
                                length += len(res)
                                sha1.update(res)
                            sha1.update(res)
                        resource, _ = Resource.objects.get_or_create(sha=sha1.hexdigest(), size=length)
                        resmap, _ = ResourceMap.objects.get_or_create(resource=resource, repo=repo, path=relpath)
                        print(path)
                    else:
                        print("exist", path)
                except OSError:
                    import traceback
                    traceback.print_exc()

                    print(path)