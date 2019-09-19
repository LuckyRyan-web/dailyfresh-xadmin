__author__ = 'LY'
__date__ = '2019/9/18 17:06'
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import *


class FDFSStorage(Storage):
    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        # 打开文件时使用
        pass
    def _save(self, name, content):
        client=Fdfs_client('./utils/fdfs/client.conf')

        # trackers = get_tracker_conf('./utils/fdfs/client.conf')
        # client = Fdfs_client(trackers)


        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FastDFS失败')

        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        """Django判断文件名是否可用"""
        return False

    def url(self, name):
        """返回访问文件url路径"""
        return self.base_url + name