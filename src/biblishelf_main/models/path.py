from django.db import models
from .repo import Repo
from .resource import Resource


class Path(models.Model):
    file_modify_time = models.DateTimeField()
    file_create_time = models.DateTimeField()
    file_access_time = models.DateTimeField()
    repo = models.ForeignKey("Repo")
    resource = models.ForeignKey("Resource")
    path = models.TextField()
    
    class Meta:
        unique_together = (
            ("repo", "resource", "path")
        )