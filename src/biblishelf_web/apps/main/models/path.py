from django.db import models
from .repo import RepoModel
from .resource import ResourceModel


class PathModel(models.Model):
    file_modify_time = models.DateTimeField()
    file_create_time = models.DateTimeField()
    file_access_time = models.DateTimeField()
    repo = models.ForeignKey("RepoModel", on_delete=models.CASCADE)
    resource = models.ForeignKey("ResourceModel", on_delete=models.CASCADE)
    path = models.TextField()
    is_exist = models.BooleanField(default=True)
    
    class Meta:
        unique_together = (
            ("repo", "resource", "path")
        )