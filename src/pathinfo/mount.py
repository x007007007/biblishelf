import os
import sys
import subprocess
import re
import sys
import psutil


def iter_mount_points(path):
    """

    >>> list(iter_mount_points("/home/xxc"))
    ...
    :param path:
    :return:
    """
    path = os.path.abspath(path)
    offset = 0
    max_len = len(path)
    while offset < max_len:
        try:
            offset = path.index(os.sep, offset) + 1
        except ValueError:
            if os.path.ismount(path):
                yield os.path.abspath(path)
                return
        if os.path.ismount(path[:offset]):
            yield os.path.abspath(path[:offset])
        offset += 1


def get_mount_info_by_df(path):
    """
    >>> get_mount_info("/Volumes/XXC-DG-SEC/")
    :param path:
    :return:
    """
    res = subprocess.check_output("df")
    for fs, mo in re.findall(r"(^/[\w/]*).*?(/.*)", res.decode(sys.getdefaultencoding()), re.M):
        if os.path.abspath(mo) == os.path.abspath(path):
            return fs

def get_mount_info(path):
    for rule in psutil.disk_partitions():
        if os.path.abspath(rule.mountpoint) == os.path.abspath(path):
            return os.path.abspath(rule.device)


def read_cmd_diskutil_list():
    """

    >>> read_cmd_diskutil_list()
    :return:
    """
    res = {}
    list_out = subprocess.check_output(["diskutil", "list"]).decode(sys.getdefaultencoding())
    for dev, infos in re.findall(r"(^/.*?)\n((?:^\s+.*?\n)+)", list_out, re.M | re.S):
        res[dev] = {}
        for pk, identifier in re.findall(r"^\s+(\d+):.*\s+([\w\d]+$)", infos, re.M):
            info_out = subprocess.check_output(["diskutil", "info", identifier]).decode(sys.getdefaultencoding())
            res[dev][identifier] = dict(re.findall(r"\s*(\S[^:]+):\s*(\S.*)$", info_out, re.M))

    return res


class PathInfo(object):
    def __init__(self):
        m = read_cmd_diskutil_list()
        # m = {'/dev/disk0': {'disk0s1': {'File System': 'None', 'OS Can Be Installed': 'No', 'Device Block Size': '512 Bytes', 'Device / Media Name': 'EFI System Partition', 'Part of Whole': 'disk0', 'Read-Only Volume': 'Not applicable (no file system)', 'Partition Type': 'EFI', 'Ejectable': 'No', 'Read-Only Media': 'No', 'Device Node': '/dev/disk0s1', 'Volume Free Space': 'Not applicable (no file system)', 'Internal': 'Yes', 'Solid State': 'Yes', 'Total Size': '209.7 MB (209715200 Bytes) (exactly 409600 512-Byte-Units)', 'SMART Status': 'Verified', 'Volume UUID': '0E239BC6-F960-3107-89CF-1C97F78BB46B', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'No', 'Media Type': 'Generic', 'Disk / Partition UUID': 'B65FD3C8-642F-4962-BDAC-9637C25F60DA', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk0s1', 'Protocol': 'PCI'}, 'disk0': {'Device Block Size': '512 Bytes', 'Device / Media Name': 'APPLE SSD SM0256G Media', 'Part of Whole': 'disk0', 'Read-Only Volume': 'Not applicable (no file system)', 'Low Level Format': 'Not supported', 'Ejectable': 'No', 'Content (IOContent)': 'GUID_partition_scheme', 'Read-Only Media': 'No', 'Device Node': '/dev/disk0', 'Volume Free Space': 'Not applicable (no file system)', 'Internal': 'Yes', 'Solid State': 'Yes', 'Total Size': '251.0 GB (251000193024 Bytes) (exactly 490234752 512-Byte-Units)', 'SMART Status': 'Verified', 'File System': 'None', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'Yes', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk0', 'Protocol': 'PCI', 'OS 9 Repos': 'No'}, 'disk0s2': {'This disk is a Core Storage Physical Volume (PV).  Core Storage Information': 'PV UUID:                  3E0ED0AF-3479-4D0B-B7D6-D0CDD575AC8B', 'OS Can Be Installed': 'No', 'Recovery Disk': 'disk0s3', 'Device / Media Name': 'Customer', 'Part of Whole': 'disk0', 'Read-Only Volume': 'Not applicable (no file system)', 'LVG UUID': 'A8AB0BD0-1562-4AB0-8DE6-07054592FF6E', 'Partition Type': 'Apple_CoreStorage', 'Ejectable': 'No', 'Read-Only Media': 'No', 'Device Node': '/dev/disk0s2', 'Internal': 'Yes', 'Volume Free Space': 'Not applicable (no file system)', 'Device Block Size': '512 Bytes', 'Solid State': 'Yes', 'Total Size': '250.1 GB (250140434432 Bytes) (exactly 488555536 512-Byte-Units)', 'SMART Status': 'Verified', 'File System': 'None', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'No', 'Media Type': 'Generic', 'Disk / Partition UUID': '25F28F59-BD5A-45BD-B448-5F424E26181A', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk0s2', 'Protocol': 'PCI'}, 'disk0s3': {'File System': 'None', 'OS Can Be Installed': 'No', 'Device Block Size': '512 Bytes', 'Device / Media Name': 'Recovery HD', 'Part of Whole': 'disk0', 'Read-Only Volume': 'Not applicable (no file system)', 'Partition Type': 'Apple_Boot', 'Ejectable': 'No', 'Read-Only Media': 'No', 'Device Node': '/dev/disk0s3', 'Volume Free Space': 'Not applicable (no file system)', 'Internal': 'Yes', 'Solid State': 'Yes', 'Total Size': '650.0 MB (650002432 Bytes) (exactly 1269536 512-Byte-Units)', 'SMART Status': 'Verified', 'Volume UUID': '98EC077A-A9F0-39ED-9B65-EEC2A98E4C4C', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'No', 'Media Type': 'Generic', 'Disk / Partition UUID': '39932904-4EBC-498E-B5BA-40618AA7FC10', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk0s3', 'Protocol': 'PCI'}}, '/dev/disk3': {'disk3': {'Device Block Size': '512 Bytes', 'Device / Media Name': 'SanDisk Cruzer Blade Media', 'Part of Whole': 'disk3', 'Read-Only Volume': 'Not applicable (no file system)', 'Low Level Format': 'Not supported', 'Ejectable': 'Yes', 'Content (IOContent)': 'FDisk_partition_scheme', 'Read-Only Media': 'No', 'Device Node': '/dev/disk3', 'Volume Free Space': 'Not applicable (no file system)', 'Internal': 'No', 'Total Size': '8.0 GB (8004304896 Bytes) (exactly 15633408 512-Byte-Units)', 'SMART Status': 'Not Supported', 'File System': 'None', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'Yes', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk3', 'Protocol': 'USB', 'OS 9 Repos': 'No'}, 'disk3s1': {'Device Block Size': '512 Bytes', 'Type (Bundle)': 'ntfs', 'Device / Media Name': 'Untitled 1', 'Mounted': 'Yes', 'Device Identifier': 'disk3s1', 'Part of Whole': 'disk3', 'Partition Type': 'Windows_NTFS', 'Ejectable': 'Yes', 'Read-Only Media': 'No', 'Device Node': '/dev/disk3s1', 'Mount Point': '/Volumes/UNTITLED', 'Volume Free Space': '283.0 MB (283049984 Bytes) (exactly 552832 512-Byte-Units)', 'Read-Only Volume': 'Yes', 'Allocation Block Size': '4096 Bytes', 'Internal': 'No', 'Total Size': '8.0 GB (8004303872 Bytes) (exactly 15633406 512-Byte-Units)', 'SMART Status': 'Not Supported', 'Volume UUID': 'A3F7C4C8-73F7-48D5-9DF2-0830F6607FCA', 'Volume Name': 'UNTITLED', 'Whole': 'No', 'Name (User Visible)': 'Windows NT File System (NTFS)', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'File System Personality': 'NTFS', 'Protocol': 'USB'}}, '/dev/disk1': {'disk1': {'Owners': 'Enabled', 'Journal': 'Journal size 24576 KB at offset 0x19502000', 'OS Can Be Installed': 'Yes', 'Recovery Disk': 'disk0s3', 'Part of Whole': 'disk1', 'Device / Media Name': 'Macintosh HD', 'Mounted': 'Yes', 'Device Identifier': 'disk1', 'LVG UUID': 'A8AB0BD0-1562-4AB0-8DE6-07054592FF6E', 'Low Level Format': 'Not supported', 'Ejectable': 'No', 'Content (IOContent)': 'Apple_HFS', 'Read-Only Media': 'No', 'This disk is a Core Storage Logical Volume (LV).  Core Storage Information': 'LV UUID:                  13C231E9-31C7-4A81-BF56-A2D92A237ED7', 'Device Node': '/dev/disk1', 'Mount Point': '/', 'Encrypted': 'Yes', 'Device Block Size': '512 Bytes', 'Internal': 'Yes', 'Volume Free Space': '38.0 GB (37965078528 Bytes) (exactly 74150544 512-Byte-Units)', 'Read-Only Volume': 'No', 'Allocation Block Size': '4096 Bytes', 'Total Size': '249.8 GB (249795969024 Bytes) (exactly 487882752 512-Byte-Units)', 'Solid State': 'Yes', 'Type (Bundle)': 'hfs', 'SMART Status': 'Not Supported', 'Volume UUID': '90462B4C-269E-3F6D-B92E-4ABDE924A0DD', 'Volume Name': 'Macintosh HD', 'Whole': 'Yes', 'Name (User Visible)': 'Mac OS Extended (Journaled)', 'Media Type': 'Generic', 'Disk / Partition UUID': '13C231E9-31C7-4A81-BF56-A2D92A237ED7', 'Fusion Drive': 'No', 'LVF UUID': 'ECF411A7-F572-42BD-8EE1-975E62DF6C79', 'File System Personality': 'Journaled HFS+', 'Protocol': 'PCI', 'OS 9 Repos': 'No'}}, '/dev/disk2': {'disk2s1': {'Device Block Size': '512 Bytes', 'Type (Bundle)': 'exfat', 'Device / Media Name': 'Untitled 1', 'Mounted': 'Yes', 'Device Identifier': 'disk2s1', 'Part of Whole': 'disk2', 'Partition Type': 'Windows_NTFS', 'Ejectable': 'Yes', 'Read-Only Media': 'No', 'Device Node': '/dev/disk2s1', 'Mount Point': '/Volumes/XXC-DG', 'Volume Free Space': '5.0 GB (5038964736 Bytes) (exactly 9841728 512-Byte-Units)', 'Read-Only Volume': 'No', 'Allocation Block Size': '32768 Bytes', 'Internal': 'No', 'Total Size': '5.1 GB (5134221312 Bytes) (exactly 10027776 512-Byte-Units)', 'SMART Status': 'Not Supported', 'Volume UUID': '2EF270D3-5F4B-36CB-893B-4DADE1A693D3', 'Volume Name': 'XXC-DG', 'Whole': 'No', 'Name (User Visible)': 'ExFAT', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'File System Personality': 'ExFAT', 'Protocol': 'USB'}, 'disk2': {'Device Block Size': '512 Bytes', 'Device / Media Name': 'TOSHIBA External USB 3.0 Media', 'Part of Whole': 'disk2', 'Read-Only Volume': 'Not applicable (no file system)', 'Low Level Format': 'Not supported', 'Ejectable': 'Yes', 'Content (IOContent)': 'FDisk_partition_scheme', 'Read-Only Media': 'No', 'Device Node': '/dev/disk2', 'Volume Free Space': 'Not applicable (no file system)', 'Internal': 'No', 'Total Size': '1.0 TB (1000204886016 Bytes) (exactly 1953525168 512-Byte-Units)', 'SMART Status': 'Not Supported', 'File System': 'None', 'Volume Name': 'Not applicable (no file system)', 'Whole': 'Yes', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'Mounted': 'Not applicable (no file system)', 'Device Identifier': 'disk2', 'Protocol': 'USB', 'OS 9 Repos': 'No'}, 'disk2s2': {'Device Block Size': '512 Bytes', 'Type (Bundle)': 'exfat', 'Device / Media Name': 'Untitled 2', 'Mounted': 'Yes', 'Device Identifier': 'disk2s2', 'Part of Whole': 'disk2', 'Partition Type': 'Windows_NTFS', 'Ejectable': 'Yes', 'Read-Only Media': 'No', 'Device Node': '/dev/disk2s2', 'Mount Point': '/Volumes/XXC-DG-SEC', 'Volume Free Space': '644.6 GB (644563206144 Bytes) (exactly 1258912512 512-Byte-Units)', 'Read-Only Volume': 'No', 'Allocation Block Size': '131072 Bytes', 'Internal': 'No', 'Total Size': '995.1 GB (995070663168 Bytes) (exactly 1943497389 512-Byte-Units)', 'SMART Status': 'Not Supported', 'Volume UUID': '6C750551-5FDE-3E99-8793-ED8E816B76C7', 'Volume Name': 'XXC-DG-SEC', 'Whole': 'No', 'Name (User Visible)': 'ExFAT', 'Media Type': 'Generic', 'OS Can Be Installed': 'No', 'File System Personality': 'ExFAT', 'Protocol': 'USB'}}}
        self.m = {}
        for k, item in m.items():
            for k1, info in item.items():
                self.m["/dev/{}".format(k1)] = info

    def get_path(self, path):
        mounts = list(iter_mount_points(path))
        for mount in mounts[::-1]:
            dev = get_mount_info(mount)
            if dev:
                vuuid = self.m[dev]["Volume UUID"]
                start = self.m[dev]["Mount Point"].rstrip("/")
                if path.startswith(start):
                    return vuuid, path[len(start):]





if __name__ == '__main__':
    pi = PathInfo()
    print(pi.get_path("/Volumes/XXC-DG-SEC/prolog中文教程.chm"))
    print(pi.get_path("/home/test.chm"))