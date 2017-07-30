from biblishelf_core.hook import ScanHooker
from biblishelf_core.shortcut import get_or_create, create_or_update
import zipfile
from biblishelf_core.file_info import FileInfo
import re
import traceback
import datetime
import chardet


class ZipScanHooker(ScanHooker):

    @staticmethod
    def hooker_base_info(mime_type, mime, extension_name):
        if extension_name in ['zip']:
            return True
        if mime_type in ['application/zip']:
            return True
        return False

    def get_fp(self, fp):
        print(fp)
        with zipfile.ZipFile(fp) as zfp:
            commit_code = chardet.detect(zfp.comment)
            print('namelist', zfp.namelist())
            for zipinfo in zfp.infolist():
                print(zipinfo.extra)
                with zfp.open(zipinfo.filename) as ifp:
                    pass

            print('comment',zfp.comment.decode(commit_code['encoding']))
