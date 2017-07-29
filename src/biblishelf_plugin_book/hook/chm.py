from biblishelf_core.hook import ScanHooker



class ChmScanHooker(ScanHooker):

    ext_name = ["chm"]

    @staticmethod
    def hooker_mime_type(mime_type, mime):
        if("application/octet-stream" == mime_type and
        "MS Windows HtmlHelp Data" == mime):
            print("get chm")
            return True
        return False

    def get_fp(self, fp):
        pass