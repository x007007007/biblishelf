from django.db import models
import os
import psutil
import json
import logging
import datetime
import pytz
import hashlib


class ResourceModel(models.Model):
    size = models.PositiveIntegerField(default=0)
    sha1 = models.CharField(max_length=224, null=True, blank=True)
    md5 = models.CharField(max_length=32, null=True, blank=True)
    ed2k_hash = models.CharField(max_length=32, null=True, blank=True)
    mime_type = models.ForeignKey("MimeTypeModel", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [("size", "sha1"), ("size", "md5"), ("size", "ed2k_hash")]

    @classmethod
    def get_or_create_from_fp(cls, fp, db=None):
        from .mime_type import MimeTypeModel
        assert fp.mode == "rb"
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        ed2k =hashlib.new('md4')
        size = 0
        fp.seek(0)

        chuck = fp.read(9500*1024)
        ed2k.update(hashlib.new('md4', chuck).digest())
        sha1.update(chuck)
        md5.update(chuck)

        mime = MimeTypeModel.get_from_chuck(chuck, db=db)

        size += len(chuck)
        while len(chuck) == 9500*1024:
            chuck = fp.read(9500*1024)
            ed2k.update(hashlib.new('md4',chuck).digest())
            sha1.update(chuck)
            md5.update(chuck)
            size += len(chuck)
        res, is_create = cls.objects.using(db).get_or_create(
            size=size,
            sha1=sha1.hexdigest(),
            md5=md5.hexdigest(),
            ed2k_hash=ed2k.hexdigest(),
            mime_type=mime
        )
        return res, is_create

    @classmethod
    def get_or_create_from_abs_path(cls, path, db=None):
        with open(path, "rb") as fp:
            return cls.get_or_create_from_fp(fp, db=db)
