from django.db import models
import os
import psutil
import json
import logging
import datetime
import pytz
import hashlib
import magic
logger = logging.Logger(__name__)
# Create your models here.


class ExtendResource(models.Model):
    name = models.CharField(max_length=64)
    resource = models.ForeignKey("biblishelf_main.Resource", null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def is_extend(self):
        return True