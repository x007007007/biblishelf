from biblishelf_core.hook import ScanHooker



class ChmScanHooker(ScanHooker):

    @staticmethod
    def hooker_base_info(mime_type, mime, extension_name):
        if extension_name.lower() in ('chm',):
            return True
        if("application/octet-stream" == mime_type and
        "MS Windows HtmlHelp Data" == mime):
            print("get chm")
            return True
        return False

    def get_fp(self, fp):
        pass