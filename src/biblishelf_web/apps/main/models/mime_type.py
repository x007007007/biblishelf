from django.db import models
import magic


class MimeTypeModel(models.Model):
    mime = models.CharField(max_length=32)
    detail = models.CharField(max_length=254)

    @classmethod
    def get_from_chuck(cls, chuck, db=None):
        obj, _ = cls.objects.using(db).get_or_create(
            mime=magic.from_buffer(chuck, mime=True),
            detail=magic.from_buffer(chuck, mime=False)
        )
        return obj