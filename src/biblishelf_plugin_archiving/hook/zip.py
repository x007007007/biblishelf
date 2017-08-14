from biblishelf_core.hook import ScanHooker
from biblishelf_core.shortcut import get_or_create, create_or_update
import zipfile
from biblishelf_core.file_info import StreamFile
import re
import traceback
import os
import time
import datetime
import chardet
from biblishelf_core.actions.scan import ContCall


class ZipContCall(ContCall):
    def __init__(self, zip_info, hooker_list):
        self.hook_list = hooker_list
        timestamp = time.mktime(zip_info.date_time+(0,0,0))
        self.create_time = datetime.datetime.utcfromtimestamp(timestamp)
        self.modify_time = self.create_time
        self.access_time = self.create_time
        self.path_name = zip_info.filename
        self.file_name = os.path.basename(self.path_name)
        self.extension_name = self.get_extension_name(self.file_name)



class ZipScanHooker(ScanHooker):

    @staticmethod
    def hooker_base_info(mime_type, mime, extension_name):
        if extension_name in ['zip']:
            return True
        if extension_name in ['epub']:
            return False
        if mime_type in ['application/zip']:
            return True
        return False

    def get_fp(self, fp):
        print(fp)
        with zipfile.ZipFile(fp) as zfp:
            commit_code = chardet.detect(zfp.comment)
            for zip_info in zfp.infolist():
                with zfp.open(zip_info.filename) as ifp:
                    with StreamFile(ifp, ZipContCall(zip_info, ScanHooker.get_hooker()), seek=False) as stream:
                        print("hello", stream.info)

