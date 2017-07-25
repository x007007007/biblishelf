import os
import io
from ..conf.repo import get_repo
from ..command import BaseCommand, CommandError
from ..models import Resource, File, Path, MimeType
import hashlib
from ..hook import ScanHooker
import magic
import uuid
import datetime


class Scan(BaseCommand):

    def handle(self, *args, **kwargs):
        repo = get_repo()
        self.repo = repo
        if repo is None:
            raise CommandError("don't have repo")
        for root, dirs, files in os.walk(os.curdir):
            for file_name in files:
                file_path = os.path.join(os.path.abspath(root), file_name)
                if (os.access(file_path, os.R_OK)):
                    try:
                        self.load_file(file_path=file_path)
                    except io.UnsupportedOperation:
                        pass

    @staticmethod
    def iter_file_chunk(file_path):
        chunk_size = 9500 * 1024
        print(file_path)
        with open(file_path, "rb") as fp:
            chuck = fp.read(chunk_size)
            yield chuck
            while (len(chuck) == chunk_size):
                chuck = fp.read(chunk_size)
                yield chuck

    def load_file(self, file_path):
        chunks = self.iter_file_chunk(file_path=file_path)
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        ed2k = hashlib.new('md4')
        mime_type = None
        size = 0
        for chunk in chunks:
            ed2k.update(hashlib.new('md4', chunk).digest())
            sha1.update(chunk)
            md5.update(chunk)
            size += len(chunk)
            if mime_type is None:
                mime_type = magic.from_buffer(chunk, mime=True)
                file_type = magic.from_buffer(chunk)
        session = self.repo.Session()
        mime_type = session.query(MimeType).filter_by(
            mime=mime_type,
            full_mime=file_type
        ).first()
        if not mime_type:
            mime_type = MimeType(
                mime=mime_type,
                full_mime=file_type
            )
            session.add(mime_type)
        resource = session.query(Resource).filter_by(
            name=os.path.basename(file_path)
        ).first()
        if not resource:
            resource = Resource(
                uuid=uuid.uuid4().hex,
                name=os.path.basename(file_path),
                create_time=datetime.datetime.now()
            )
            session.add(resource)

        resource_file = session.query(File).filter_by(
            size=size,
            md5=md5.hexdigest(),
            ed2k=ed2k.hexdigest()
        ).first()
        if not resource_file:
            resource_file = File(
                size=size,
                md5=md5.hexdigest(),
                ed2k=ed2k.hexdigest(),
                sha1=sha1.hexdigest(),
                resource=resource,
                mime_type=mime_type
            )
            session.add(resource_file)

        resource_file_path = session.query(Path).filter_by(
            path=file_path
        ).first()
        if not resource_file_path:
            resource_file_path = Path(
                path=file_path
            )
            session.add(resource_file_path)

        session.commit()



