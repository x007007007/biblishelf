from django.db import models


class SubRepo(models.Model):
    repo = models.ForeignKey("Repo", on_delete=models.CASCADE)
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE)
    