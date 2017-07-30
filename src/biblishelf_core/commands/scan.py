import os
import io
from ..conf.repo import get_repo
from ..command import BaseCommand, CommandError
from ..models import Resource, File, Path, MimeType
import hashlib
from ..hook import ScanHooker
import magic
import uuid
from ..shortcut import create_or_update, get_or_create
import datetime


class Scan(BaseCommand):

    def handle(self, *args, **kwargs):
        self.hook_list = ScanHooker.get_hooker()
        repo = get_repo()
        self.repo = repo
        session = self.repo.Session()
        if repo is None:
            raise CommandError("don't have repo")
        for root, dirs, files in os.walk(os.curdir):
            for file_name in files:
                if file_name.startswith("."):
                    continue
                file_path = os.path.join(os.path.abspath(root), file_name)
                if (os.access(file_path, os.R_OK)):
                    record = session.query(Path).filter_by(
                        path=file_path
                    ).first()
                    disk_time = datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime)
                    if record and record.modify_time != disk_time:
                        continue
                    try:
                        self.load_file(file_path=file_path)
                    except io.UnsupportedOperation:
                        pass

    @staticmethod
    def iter_file_chunk(file_path):
        chunk_size = 9500 * 1024
        with open(file_path, "rb") as fp:
            chuck = fp.read(chunk_size)
            yield chuck
            while (len(chuck) == chunk_size):
                chuck = fp.read(chunk_size)
                yield chuck

    def is_hook_by_mime_type_and_name(self, mime_type, mime, name):
        extension_names = name.lstrip(".").split(".")
        if len(extension_names) > 1:
            extension_name = extension_names[-1]
        else:
            extension_name = ""
        for hookcls in self.hook_list:
            assert issubclass(hookcls, ScanHooker)
            if hookcls.hooker_base_info(mime_type, mime, extension_name):
                return True
        return False


    def hook_deal(self, file_path, resource, mime_type, mime, name):
        with open(file_path, 'rb') as fp:
            for hookcls in self.hook_list:
                if hookcls.hooker_base_info(mime_type, mime, name):
                    fp.seek(0)
                    hookobj = hookcls(resource)
                    hookobj.get_fp(fp)

    def load_file(self, file_path):
        chunks = self.iter_file_chunk(file_path=file_path)
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        ed2k = hashlib.new('md4')
        mime_type = None
        size = 0
        file_type = None
        for chunk in chunks:
            ed2k.update(hashlib.new('md4', chunk).digest())
            sha1.update(chunk)
            md5.update(chunk)
            size += len(chunk)
            if mime_type is None:
                mime_type = magic.from_buffer(chunk, mime=True)
                file_type = magic.from_buffer(chunk)
                if not self.is_hook_by_mime_type_and_name(
                        mime_type,
                        file_type,
                        os.path.basename(file_path)
                ):
                    return False

        session = self.repo.Session()

        mimetype, _ = get_or_create(
            session, MimeType,
            mime=mime_type,
            full_mime=file_type
        )
        resource, _ = get_or_create(
            session, Resource,
            default={
                "uuid": uuid.uuid4().hex,
                "create_time": datetime.datetime.now()
            },
            name=os.path.basename(file_path).strip()
        )

        resource_file, _ = get_or_create(
            session, File,
            default={
                "sha1": sha1.hexdigest(),
                "resource": resource,
                "mime_type": mimetype
            },
            size=size,
            md5=md5.hexdigest(),
            ed2k=ed2k.hexdigest()
        )
        stat = os.stat(file_path)
        resource_file_path, _ = create_or_update(
            session, Path,
            default={
                "file_id": resource_file.id,
                "modify_time": datetime.datetime.fromtimestamp(stat.st_mtime),
                "create_time": datetime.datetime.fromtimestamp(stat.st_ctime),
                "access_time": datetime.datetime.fromtimestamp(stat.st_atime),
            },
            path=file_path,
        )

        self.hook_deal(
            file_path,
            resource,
            mime_type,
            file_type,
            os.path.basename(file_path)
        )


