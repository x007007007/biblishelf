import json

from django.db import models, router
import os
import time
import datetime
import pytz
from django.db import connections
import toml


class RepoHashModel(models.Model):
    """
    记录历史上这个repo用过的hash
    """
    uuid = models.CharField(max_length=254)
    repo = models.ForeignKey("RepoModel", on_delete=models.CASCADE)

