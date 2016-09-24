from django.core.management.base import BaseCommand, CommandError
from biblishelf_main.models import ConfigWatchArea, Driver, ResourceMap, Resource
import os
import psutil
import json
import warnings
import uuid
import datetime
import pytz
from pyudev import Context, Monitor
import platform
import time
import logging
import logging.config


from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.Logger(__name__)


class MountPointOnMacEventHandler(FileSystemEventHandler):
    resource_map = None

    def __init__(self, paths):
        self.mount_path = paths

    def dispatch(self, event):
        if os.path.basename(event.src_path).startswith("._"):
            return
        self.resource_map = ResourceMap.find_by_abs_path(event.src_path)
        print(event.src_path)
        super(MountPointEventHandler, self).dispatch(event)

    def on_any_event(self, event):
        print(self.resource_map)

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
        {
            "Darwin": self.monitor_mac
        }[platform.system()]()

    def monitor_mac(self):
        observer = Observer()
        paths = [e.get_mount_path() for e in Driver.objects.all() if e.get_mount_path() is not None]
        event_handler = MountPointEventHandler(paths)
        for path in paths:
            observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                logger.debug("check storage mount")
                if Driver.refresh_mount_db():
                    if observer.is_alive():
                        observer.stop()
                    paths = [e.get_mount_path() for e in Driver.objects.all() if e.get_mount_path() is not None]
                    event_handler = MountPointOnMacEventHandler(paths)
                    for path in paths:
                        observer.schedule(event_handler, path, recursive=True)
                    observer.start()
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()