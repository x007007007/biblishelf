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


class RopeNotExist(models.ObjectDoesNotExist): pass


class Repo(models.Model):
    META_PATH = ".biblishelf/disk.json"
    MOUNT = "mount"
    USER_SET = "set"
    name = models.CharField(max_length=128, blank=True, null=True)
    uuid = models.CharField("Volumn", max_length=128)
    type = models.CharField(
        choices=(
            (MOUNT, MOUNT),
            (USER_SET, USER_SET),
        ),
        max_length=32,
        null=True,
        blank=True
    )
    dev_path = models.CharField(max_length=128, null=True, blank=True)
    fs = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    extend_info = models.TextField(
        null=True,
        blank=True
    )
    online_status = models.NullBooleanField(
        null=True,
        blank=True
    )
    last_online_time = models.DateTimeField(auto_now_add=True, null=True)
    uri = models.CharField(max_length=254, null=True, blank=True)

    @classmethod
    def refresh_mount_db(cls):
        """
        refresh mount info ,check new storage repo
        :return: found new mount event
        """
        logger.debug("refresh_mount_db")
        update_num = 0
        for partition in psutil.disk_partitions(all=True):
            logging.debug("partition", partition)
            if cls.objects.filter(uri=partition.mountpoint, dev_path=partition.device).count() == 1:
                continue
            else:
                meta_path = os.path.join(partition.mountpoint, cls.META_PATH)
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path) as fp:
                            puid = json.load(fp).get("uuid")
                            logger.debug("find puid", puid)
                            if puid:
                                update_num += cls.objects.filter(   # how many exists repo change mountpoint info
                                    models.Q(uuid=puid),
                                    ~models.Q(uri=partition.mountpoint, dev_path=partition.device)
                                ).update(
                                    uri=partition.mountpoint,
                                    dev_path=partition.device,
                                    last_online_time=datetime.datetime.now(pytz.UTC),
                                )
                                if cls.objects.filter(uuid=puid).count() == 0:  # some don't exits in db
                                    cls(
                                        uuid=puid,
                                        uri=partition.mountpoint,
                                        dev_path=partition.device,
                                        last_online_time=datetime.datetime.now(pytz.UTC),
                                    ).save()
                                    update_num += 1
                    except (json.JSONDecodeError, PermissionError, FileNotFoundError) as e:
                        import traceback
                        traceback.print_exc()
                        continue
        if update_num > 0:
            return True
        return False

    def is_online(self):
        """
        :return: bool
        """
        return self.online_status

    def get_mount_path(self):
        if os.path.exists(self.get_meta_path()):
            return self.uri if self.uri.endswith(os.sep) else self.uri + os.sep
        else:
            self.uri = None
            self.save(update_fields=["uri"])
        return None

    def get_meta_path(self):
        return os.path.join(self.uri, self.META_PATH)


class Resource(models.Model):
    size = models.PositiveIntegerField(default=0)
    sha = models.CharField(max_length=150, null=True, blank=True)
    md5 = models.CharField(max_length=32, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    mine_type = models.CharField(max_length=32, null=True, blank=True)
    ed2k_hash = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        unique_together = ["size", "sha"]

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


class ResourceMap(models.Model):
    resource = models.ForeignKey(Resource, related_name="Map", null=True)
    path = models.CharField(max_length=1024)
    repo = models.ForeignKey(Repo, related_name='Resources')
    create_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")
    modify_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")

    @classmethod
    def create_or_update_by_abs_path(cls, path, ropes=None):
        if ropes is None:
            ropes = list(Repo.objects.all())
        for repo in sorted(ropes, key=lambda x: len(x.uri), reverse=True):
            if path.startswith(repo.get_mount_path()):
                res, _ = Resource.get_or_create_from_abs_path(path)
                resmap, is_create = ResourceMap.objects.update_or_create(
                    path=path[len(repo.uri):],
                    repo=repo,
                    resource=res,
                    defaults={
                        "create_time": datetime.datetime.fromtimestamp(os.path.getctime(path), tz=pytz.UTC),
                        "modify_time": datetime.datetime.fromtimestamp(os.path.getmtime(path), tz=pytz.UTC)
                    }
                )
                return resmap
        raise RopeNotExist()

    @classmethod
    def find_by_abs_path(cls, path):
        res = []
        for repo in Repo.objects.all():
            mpath = repo.get_mount_path()
            if mpath and path.startswith(mpath):
                subpath = path[len(mpath)]
                try:
                    resmap = cls.objects.get(repo=repo, path=subpath)  # type: ResourceMap
                    res.append((len(mpath), resmap))
                except:
                    pass
        if len(res) > 0:
            res.sort(key=lambda x: x[0], reverse=True)
            return res[0][1]
        else:
            return None

    def get_abs_path(self):
        if self.path.startswith(os.sep):
            self.path = self.path[1:]
            self.save(update_fields=["path"])
        return os.path.join(self.repo.get_mount_path(), self.path)


class ResourceAuthor(models.Model):
    name = models.CharField(max_length=32)


class ExtendResource(models.Model):
    name = models.CharField(max_length=64)
    resource = models.ForeignKey(Resource, null=True)

    class Meta:
        abstract = True

    def is_extend(self):
        return True


class ConfigWatchArea(models.Model):
    repo = models.ForeignKey(Repo, related_name="WatchAreas")
    path = models.CharField(max_length=1024)