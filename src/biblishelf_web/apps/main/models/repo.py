import json

from django.db import models, router
import os
import time
import datetime
import pytz
from django.db import connections
import toml


class RepoModel(models.Model):
    name = models.CharField(null=True, blank=True, max_length=254)
    uuid = models.UUIDField(unique=True, null=False)
    is_main = models.BooleanField(default=False)
    is_portable = models.BooleanField(default=True)
    auto_sync = models.BooleanField(default=True)
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
    def load_database_from_path(cls, curp):
        """
        django 连接数据库
        """
        root_path = cls.get_repo_root_from_path(curp)
        meta = cls.get_repo_meta_form_root(root_path)
        m_uuid = meta['uuid']
        connections.databases[m_uuid] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(root_path, ".bibrepo\index.sqlite3"),
        }
        return m_uuid

    @classmethod
    def migrate(cls, root):
        meta = cls.get_repo_meta_form_root(root)
        pass


    @classmethod
    def save_repo_meta(cls, config, root):
        repo_meta_path = os.path.join(root, '.bibrepo/meta.json')
        repo_meta_toml_path = os.path.join(root, '.bibrepo/meta.toml')
        old_config = cls.get_repo_meta_form_root(root)
        old_config.update(config)
        with open(repo_meta_path, 'w', encoding='utf-8') as fp:
            json.dump(old_config, fp)
        with open(repo_meta_toml_path, 'w', encoding='utf-8') as fp:
            toml.dump(old_config, fp)

    @classmethod
    def get_repo_meta_form_root(cls, root):
        repo_meta_path = os.path.join(root, '.bibrepo/meta.json')
        repo_meta_toml_path = os.path.join(root, '.bibrepo/meta.toml')
        if os.path.exists(repo_meta_toml_path):
            with open(repo_meta_toml_path) as fp:
                return toml.load(fp)
        elif os.path.exists(repo_meta_path):
            with open(repo_meta_path) as fp:
                return json.load(fp)


    @classmethod
    def get_repo_root_from_path(cls, curp):
        repo_meta_path = os.path.join(curp, '.bibrepo/meta.json')
        repo_meta_toml_path = os.path.join(curp, '.bibrepo/meta.toml')
        if os.path.exists(repo_meta_toml_path):
            return curp
        elif os.path.exists(repo_meta_path):
            return curp
        if (parent_path := os.path.dirname(curp)) != curp:
            return cls.get_repo_root_from_path(parent_path)

    @classmethod
    def get_repo_form_path(cls, curp, db):
        repo_root = cls.get_repo_root_from_path(curp)
        meta = cls.get_repo_meta_form_root(repo_root)
        return cls.objects.using(db).get_or_create(
            defaults=dict(
                name=meta['repo'],
            ),
            uuid=meta['uuid'],
        )[0]

    def add_file(self, db, root_path, file_path):
        from .resource import ResourceModel
        from .path import PathModel
        file_path = os.path.abspath(file_path)
        root_path = os.path.abspath(root_path)
        resource, _ = ResourceModel.get_or_create_from_abs_path(file_path, db=db)
        path, _ = PathModel.objects.using(db).get_or_create(
            defaults=dict(
                file_modify_time=datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=pytz.utc),
                file_create_time=datetime.datetime.fromtimestamp(os.path.getctime(file_path), tz=pytz.utc),
                file_access_time=datetime.datetime.fromtimestamp(os.path.getatime(file_path), tz=pytz.utc),
            ),
            repo=self,
            resource=resource,
            path=file_path[len(root_path):].lstrip(os.path.sep)
        )
        return resource, path

    def iter_resource_abspath(self, db, base_root):
        assert os.path.exists(os.path.join(base_root, '.bibrepo/meta.json'))
        from .resource import ResourceModel
        from .path import PathModel
        for resource in ResourceModel.objects.using(db).filter(pathmodel__repo=self):
            if res := resource.pathmodel_set.using(db).order_by('-file_access_time').first():
                assert isinstance(res, PathModel), type(res)
                yield resource, os.path.join(base_root, res.path)
            else:
                print(f'{resource} no path')
