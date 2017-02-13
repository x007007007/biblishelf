from django.db import models
import os
import psutil
import json
import logging
import datetime
import pytz
import hashlib
import magic


class Resource(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    size = models.PositiveIntegerField(default=0)
    sha1 = models.CharField(max_length=224, null=True, blank=True)
    md5 = models.CharField(max_length=32, null=True, blank=True)
    ed2k_hash = models.CharField(max_length=32, null=True, blank=True)
    mine_type = models.ForeignKey("MineType", null=True, blank=True)

    class Meta:
        unique_together = [("size", "sha1"), ("size", "md5"), ("size", "ed2k_hash")]

    @classmethod
    def get_or_create_from_fp(cls, fp):
        assert fp.mode == "rb"
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        ed2k =hashlib.new('md4')
        mine_type = None
        size = 0
        fp.seek(0)

        chuck = fp.read(9500*1024)
        ed2k.update(hashlib.new('md4', chuck).digest())
        sha1.update(chuck)
        md5.update(chuck)
        mine_type = magic.from_buffer(chuck)
        size += len(chuck)
        while len(chuck) == 9500*1024:
            chuck = fp.read(9500*1024)
            ed2k.update(hashlib.new('md4',chuck).digest())
            sha1.update(chuck)
            md5.update(chuck)
            size += len(chuck)
        res, is_create = cls.objects.get_or_create(
            size=size,
            sha=sha1.hexdigest(),
            md5=md5.hexdigest(),
            ed2k_hash=ed2k.hexdigest(),
            mine_type=mine_type
        )
        return res, is_create

    @classmethod
    def get_or_create_from_abs_path(cls, path):
        with open(path, "rb") as fp:
            return cls.get_or_create_from_fp(fp)