from ..file_info import ContCallBroken, BaseContCall
import os
import datetime

class ContCall(BaseContCall):
    is_checked = False

    def __init__(self, filepath, hook_list):
        self.hook_list = hook_list
        self.file_name = os.path.basename(filepath)
        stat = os.stat(filepath)
        self.create_time = datetime.datetime.fromtimestamp(stat.st_ctime)
        self.modify_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        self.access_time = datetime.datetime.fromtimestamp(stat.st_atime)
        self.extension_name = self.get_extension_name(self.file_name)

    def __call__(self, chunk, res):
        if self.is_checked:
            return True
        else:
            self.is_checked = True
            mime = res.get("mime", {})
            print(mime)
            for hookcls in self.hook_list:
                if hookcls.hooker_base_info(
                    mime.get("type"),
                    mime.get("full"),
                    self.extension_name
                ):
                    return True
            raise ContCallBroken