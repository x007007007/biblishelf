from django.db import models


class MineType(models.Model):
    mine = models.CharField(max_length=32)
    detail = models.CharField(max_length=254)