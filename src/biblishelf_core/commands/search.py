import os
import io
from sqlalchemy import or_
from ..conf.repo import get_repo
from ..command import BaseCommand, CommandError
from ..models import Resource, File, Path, MimeType
import hashlib
from ..hook import SearchHooker
import magic
import uuid
from ..shortcut import get_or_create
import datetime


class Search(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'key',
            help='search resource'
        )
        parser.add_argument(
            '-t', '--type',
            help="file type",
            default=None,
        )
        parser.add_argument(
            '-p', '--path',
            help="search select path, default is current path",
            default=os.path.abspath(os.curdir)
        )
        parser.add_argument(
            '--all',
            help="search whole repo"
        )


    def handle(self, arg, *args, **kwargs):
        self.search_text = arg.key
        self.arg = arg
        self.hook_list = SearchHooker.get_hooker()
        repo = get_repo()
        self.repo = repo
        if repo is None:
            raise CommandError("don't have repo")

        self.search(self.search_text)


    def search(self, key):
        session = self.repo.Session()
        resources = session.query(Path, Resource, File).join(
            Path.file
        ).join(
            File.mime_type
        ).join(
            File.resource
        ).filter(
            or_(
                Resource.name.like("%{}%".format(key)),
                Path.path.like("%{}%".format(key))
            )
        )
        if (self.arg.type is not None):
            resources = resources.filter(
                or_(
                    MimeType.mime.like("%{}%".format(self.arg.type)),
                    MimeType.full_mime.like("%{}%".format(self.arg.type))
                )
            ).group_by(
                Resource.name,
            )
        for path, res, finfo in resources.all():
            print(res.name, path.path, finfo.md5)
        self.hook_deal(key)



    def hook_deal(self, key):
        for hookcls in self.hook_list:
            hookobj = hookcls()
            hookobj.search(key)


