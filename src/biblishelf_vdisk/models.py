from django.db import models
from biblishelf_main.models import Resource, Driver, ExtendResource
# Create your models here.


def _vdisk_cover_uploader(*args):
    print(*args)


class VDisk(ExtendResource):
    driver = models.ForeignKey(Driver, null=True, blank=True)
    uuid = models.CharField("Volumn", max_length=128, null=True)
    type = models.CharField(
        max_length=32,
    )
    cover = models.ImageField("cover", upload_to=_vdisk_cover_uploader)
    file_number = models.PositiveIntegerField(default=0)
    info = models.TextField()



