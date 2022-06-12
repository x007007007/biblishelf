from django.db import models
import logging
logger = logging.Logger(__name__)
# Create your models here.


class RepoConfigModel(models.Model):
    path = models.CharField(max_length=254)
