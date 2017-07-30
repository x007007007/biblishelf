import magic
import hashlib


class ContCallBroken(Exception):
    pass


class FileInfo(object):

    def __init__(self, fp, contcall, seek=True):
        self.fp = fp
        self.contcall = contcall
        if seek:
            fp.seek(0)

    def __enter__(self):
        self._chunks = self._split_chunk()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True
        if issubclass(exc_type, ContCallBroken) or exc_type == ContCallBroken:
            return True

    def _split_chunk(self):
        chunk_size = 9500 * 1024
        chuck = self.fp.read(chunk_size)
        yield chuck
        while (len(chuck) == chunk_size):
            chuck = self.fp.read(chunk_size)
            yield chuck

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

    @property
    def info(self):
        for _ in self.iter_chuck():
            pass
        return self._res
