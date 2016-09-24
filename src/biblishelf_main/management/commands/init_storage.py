from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import ConfigWatchArea, Repo, ResourceMap, Resource
import os
import psutil
import json
import warnings
import uuid
import datetime
import pytz


class Command(BaseCommand):
    help = ''

    @staticmethod
    def load_or_create_disk_conf(conf_path):
        """

        :param conf_path:
        :return:
        """
        if os.path.exists(conf_path):
            try:
                with open(conf_path) as fp:
                    conf = json.load(fp)
                    return conf
            except (PermissionError, json.JSONDecodeError, IOError):
                warnings.warn("load conf failure", ResourceWarning)
        try:
            if not os.path.exists(os.path.dirname(conf_path)):
                os.makedirs(os.path.dirname(conf_path))
            with open(conf_path, "w") as fp:
                conf = {
                    "uuid": uuid.uuid4().hex
                }
                json.dump(conf, fp)
                return conf
        except (PermissionError, json.JSONDecodeError, IOError):
            warnings.warn("init conf failure", ResourceWarning)
        raise RecursionError

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for partition in psutil.disk_partitions():
            conf_path = os.path.join(partition.mountpoint, ".biblishelf/disk.json")
            try:
                conf = self.load_or_create_disk_conf(conf_path)
            except RecursionError as e:
                continue
            repo, created = Repo.objects.get_or_create(uuid=conf["uuid"])
            if created:
                repo.uri = partition.mountpoint
                dirver.fs = partition.fstype
                repo.save(update_fields=["uri"])
            else:
                update_fields = ["last_online_time"]
                if repo.uri != partition.mountpoint:
                    repo.uri = partition.mountpoint
                    update_fields.append("uri")
                if repo.fs != partition.fstype:
                    repo.fs = partition.fstype
                    update_fields.append('fs')
                    warnings.warn("Unexpect fstype", RuntimeWarning)
                repo.last_online_time = datetime.datetime.now(tz=pytz.UTC)
                repo.save(update_fields=update_fields)
