import magic
import hashlib
import tempfile

class ContCallBroken(Exception):
    pass


class BaseContCall(object):

    @staticmethod
    def get_extension_name(file_name):
        extension_names = file_name.lstrip(".").split(".")
        if len(extension_names) > 1:
            extension_name = extension_names[-1]
        else:
            extension_name = ""
        return extension_name

class StreamFile(object):
    _temp_file = None
    def __init__(self, fp, IterBroker, seek=True):
        self.fp = fp
        self.contcall = contcall
        self.create_time = getattr(contcall, "create_time")
        self.access_time = getattr(contcall, "access_time")
        self.modify_time = getattr(contcall, "modify_time")
        self._seek = seek
        if self._seek:
            fp.seek(0)

    def __enter__(self):
        if not self._seek:
            self._temp_file = tempfile.TemporaryFile(mode="wb")
            print("temporary file", self._temp_file)
        self._chunks = self._split_chunk()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._seek:
            self._temp_file.detach()

        if exc_type is None:
            return True
        if issubclass(exc_type, ContCallBroken) or exc_type == ContCallBroken:
            return True

    def _split_chunk(self):
        chunk_size = 9500 * 1024
        chuck = self.fp.read(chunk_size)
        yield chuck
        if not self._seek:
            self._temp_file.write(chuck)
        while (len(chuck) == chunk_size):
            chuck = self.fp.read(chunk_size)
            yield chuck
            if not self._seek:
                self._temp_file.write(chuck)
        if not self._seek:
            self._temp_file.flush()

    def iter_chuck(self):
        md5 = True
        ed2k = True
        sha1 = True
        size = True
        mime = True
        self._res = {}
        res = self._res
        if md5:
            res['md5'] = hashlib.md5()
        if ed2k:
            res['ed2k'] = hashlib.new('md4')
        if sha1:
            res['sha1'] = hashlib.sha1()
        if size:
            res['size'] = 0
        if mime:
            res['mime'] = None
        for chunk in self._chunks:
            yield chunk
            if md5:
                res['md5'].update(chunk)
            if ed2k:
                res['ed2k'].update(hashlib.new('md4', chunk).digest())
            if sha1:
                res['sha1'].update(chunk)
            if size:
                res['size'] += len(chunk)
            if mime and res['mime'] is None:
                res['mime'] = {
                    "type": magic.from_buffer(chunk, mime=True),
                    "full": magic.from_buffer(chunk)
                }
            self.contcall(chunk, res)

    def get_fp(self):
        if self._seek:
            self.fp.seek(0)
            return self.fp
        else:
            self._temp_file.seek()
            return self._temp_file

    @property
    def info(self):
        for _ in self.iter_chuck():
            pass
        return self._res
