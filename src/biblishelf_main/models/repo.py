import json

from django.db import models
import os
import time
import datetime
import pytz


class RepoModel(models.Model):
    name = models.CharField(null=True, blank=True, max_length=254)
    uuid = models.UUIDField(unique=True, null=False)
    is_main = models.BooleanField(default=False)
    is_portable = models.BooleanField(default=True)
    media_type = models.CharField(
        choices=(
            ("disc", "disc"),
            ("ssd", "ssd"),
            ("usb-disc", "usb-disc"),
            ("cd", "cd"),
            ("usb-ssd", 'usb-ssd'),
            ("tf/sd", "tf-sd"),
            ("samba", "samba"),
            ("cloud", "cloud")
        ),
        max_length=32
    )

    @classmethod
    def get_repo_root_from_path(cls, curp):
        repo_meta_path = os.path.join(curp, '.bibrepo/meta.json')
        if os.path.exists(repo_meta_path):
            return curp
        if (parent_path := os.path.dirname(curp)) != curp:
            return cls.get_repo_root_from_path(parent_path)

    @classmethod
    def get_repo_form_path(cls, curp):
        repo_root = cls.get_repo_root_from_path(curp)
        repo_meta_path = os.path.join(repo_root, '.bibrepo/meta.json')
        if os.path.exists(repo_meta_path):
            with open(repo_meta_path) as fp:
                meta = json.load(fp)
                return cls.objects.get_or_create(
                    defaults=dict(
                        name=meta['repo'],
                    ),
                    uuid=meta['uuid'],
                )[0]


    def add_file(self, root_path, file_path):
        from .resource import ResourceModel
        from .path import PathModel
        file_path = os.path.abspath(file_path)
        root_path = os.path.abspath(root_path)
        resource, _ = ResourceModel.get_or_create_from_abs_path(file_path)
        path, _ = PathModel.objects.get_or_create(
            defaults=dict(
                file_modify_time=datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=pytz.utc),
                file_create_time=datetime.datetime.fromtimestamp(os.path.getctime(file_path), tz=pytz.utc),
                file_access_time=datetime.datetime.fromtimestamp(os.path.getatime(file_path), tz=pytz.utc),
            ),
            repo=self,
            resource=resource,
            path=file_path[len(root_path):].lstrip('/')
        )
        return resource, path

    def iter_resource_abspath(self, base_root):
        assert os.path.exists(os.path.join(base_root, '.bibrepo/meta.json'))
        from .resource import ResourceModel
        from .path import PathModel
        for resource in ResourceModel.objects.filter(pathmodel__repo=self):
            res = resource.pathmodel_set.order_by('-file_access_time').first()
            assert isinstance(res, PathModel)
            yield os.path.join(base_root, res.path)


