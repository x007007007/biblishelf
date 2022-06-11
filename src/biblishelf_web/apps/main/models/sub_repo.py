from django.db import models


class SubRepoModel(models.Model):
    repo = models.ForeignKey("RepoModel", on_delete=models.CASCADE)
    resource = models.ForeignKey("ResourceModel", on_delete=models.CASCADE)
    