from biblishelf_core.hook import ScanHooker
from biblishelf_core.shortcut import get_or_create, create_or_update
import zipfile
import re
import traceback
import datetime


class ZipScanHooker(ScanHooker):

    @staticmethod
    def hooker_base_info(mime_type, mime, extension_name):
        if extension_name in ['zip']:
            print(mime_type, mime)
            return True
        return False

    def get_fp(self, fp):
        print(fp)
        with zipfile.ZipFile(fp) as zfp:
            print('namelist', zfp.namelist())
            print('infolist', zfp.infolist())
            print('getinfo', zfp.getinfo())
            print('comment',zfp.comment)
