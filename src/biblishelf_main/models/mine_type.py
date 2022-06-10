from django.db import models


class MineTypeModel(models.Model):
    mine = models.CharField(max_length=32)
    detail = models.CharField(max_length=254)