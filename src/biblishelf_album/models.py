from django.db import models
from biblishelf_main.models import ExtendResource, ResourceAuthor
# Create your models here.


class Album(ExtendResource):
    author = models.ForeignKey(ResourceAuthor, null=True, blank=True)


class AlbumTrick(ExtendResource):
    album = models.ForeignKey(Album)
    duration = models.DurationField()