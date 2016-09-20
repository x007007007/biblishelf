from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import ConfigWatchArea, Driver, ResourceMap, Resource
from biblishelf_vdisk.models import VDisk
from pathinfo import mount
import os
import hashlib
pi = mount.PathInfo()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for wa in ConfigWatchArea.objects.all():
            for root, dirs, files in os.walk(wa.path):
                for file in [file for file in files if file.endswith(".pdf")]:
                    path = os.path.join(root, file)
                    vol, relpath = pi.get_path(path)
                    driver, _ = Driver.objects.get_or_create(uuid=vol)
                    try:
                        if ResourceMap.objects.filter(driver=driver, path=relpath).count() == 0:
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
                            resmap, _ = ResourceMap.objects.get_or_create(resource=resource, driver=driver, path=relpath)
                            print(path)
                        else:
                            print("exist", path)
                    except OSError:
                        import traceback
                        traceback.print_exc()

                        print(path)