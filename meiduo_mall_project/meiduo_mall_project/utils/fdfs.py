"""
重写Django后端文件存储类
"""
from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """
    自定义文件存储系统，修改存储方案
    """
    def url(self, name):

        return settings.FDFS_BASE_URL + name
