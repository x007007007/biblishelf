import os
import io
from ..conf.repo import get_repo
from ..command import BaseCommand, CommandError
from ..models import Resource, File, Path, MimeType
from ..hook import ScanHooker
import uuid
from ..shortcut import create_or_update, get_or_create
import datetime
from ..file_info import StreamFile
from ..actions.scan import ContCall


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

    def hook_deal(self, fp, file_path, resource, mime_type, mime, name):
        for hookcls in self.hook_list:
            if hookcls.hooker_base_info(mime_type, mime, name):
                hookobj = hookcls(resource)
                hookobj.get_fp(fp)


    def generate_table(self, file_path, res, stream):
        session = self.repo.Session()
        mimetype, _ = get_or_create(
            session, MimeType,
            mime=res['mime']['type'],
            full_mime=res['mime']['full']
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
                "sha1": res['sha1'].hexdigest(),
                "resource": resource,
                "mime_type": mimetype
            },
            size=res['size'],
            md5=res['md5'].hexdigest(),
            ed2k=res['ed2k'].hexdigest()
        )
        resource_file_path, _ = create_or_update(
            session, Path,
            default={
                "file_id": resource_file.id,
                "modify_time": stream.modify_time,
                "create_time": stream.create_time,
                "access_time": stream.access_time,
            },
            path=file_path,
        )
        session.commit()
        return resource

    def load_file(self, file_path):
        with open(file_path, 'rb') as fp:
            with StreamFile(fp, ContCall(file_path, self.hook_list)) as stream:
                res = stream.info
                resource = self.generate_table(file_path, res, stream)

                self.hook_deal(
                    stream.get_fp(),
                    file_path,
                    resource,
                    res['mime']['type'],
                    res['mime']['full'],
                    os.path.basename(file_path)
                )






