from django.db import models


class HashSha(models.Model):
    frag1 = models.CharField(max_length=254)
    frag2 = models.CharField(max_length=254)
    frag3 = models.CharField(max_length=130)
    frag4 = models.CharField(max_length=4)
    frag5 = models.CharField(max_length=2)
    resource = models.OneToOneField(
        "Resource",
        on_delete=models.CASCADE
    )