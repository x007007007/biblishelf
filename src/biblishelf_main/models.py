from django.db import models
import os
import psutil
import json
import logging
import datetime
import pytz
logger = logging.Logger(__name__)
# Create your models here.


class Driver(models.Model):
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
                                update_num += cls.objects.filter(
                                    models.Q(uuid=puid),
                                    ~models.Q(uri=partition.mountpoint, dev_path=partition.device)
                                ).update(
                                    uri=partition.mountpoint,
                                    dev_path=partition.device,
                                    last_online_time=datetime.datetime.now(pytz.UTC),
                                )
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
            return self.uri
        else:
            self.uri = None
            self.save(update_fields=["uri"])
        return None

    def get_meta_path(self):
        return os.path.join(self.uri, self.META_PATH)


class Resource(models.Model):
    size = models.PositiveIntegerField(default=0)
    sha = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    mine_type = models.CharField(max_length=32, null=True, blank=True)
    ed2k_hash = models.CharField(max_length=32, null=True, blank=True)


class ResourceMap(models.Model):
    resource = models.ForeignKey(Resource, related_name="Map", null=True)
    path = models.CharField(max_length=1024)
    driver = models.ForeignKey(Driver, related_name='Resources')
    create_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")
    modify_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")

    @classmethod
    def find_by_abs_path(cls, path):
        res = []
        for driver in Driver.objects.all():
            mpath = driver.get_mount_path()
            if mpath and path.startswith(mpath):
                subpath = path[len(mpath)]
                try:
                    resmap = cls.objects.get(driver=driver, path=subpath)  # type: ResourceMap
                    res.append((len(mpath), resmap))
                except:
                    pass
        if len(res) > 0:
            res.sort(key=lambda x: x[0], reverse=True)
            return res[0][1]
        else:
            return None

    def get_abs_path(self):
        return os.path.join(self.driver.get_path(), self.path)


class ResourceAuthor(models.Model):
    name = models.CharField(max_length=32)


class ExtendResource(models.Model):
    name = models.CharField(max_length=64)
    resource = models.ForeignKey(ResourceMap, null=True)

    class Meta:
        abstract = True


class ConfigWatchArea(models.Model):
    driver = models.ForeignKey(Driver, related_name="WatchAreas")
    path = models.CharField(max_length=1024)