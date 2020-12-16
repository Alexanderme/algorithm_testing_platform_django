"""
    #  @ModuleName: upload_download_file
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/10 19:56
"""
import os
import logging
from django.http import StreamingHttpResponse

logger = logging.getLogger(__name__)


def upload_file(requests, save_dir):
    """
    用于处理上传文件 ,保存到指定目录
    :return:
    """
    File = requests.FILES.get('file_name')
    file_with_dir = os.path.join(save_dir, File.name)
    if File is None:
        logging.exception(File)
        return False
    else:
        with open(file_with_dir, 'wb+') as f:
            for chunk in File.chunks():
                f.write(chunk)
        return True, file_with_dir


def download_file(file):
    """
    用于处理下载文件, 当前方式用于小于500M的文件下载
    大文件下载需要单独的nginx来支持不然会出现flask相同的下载问题
    :return:
    """
    def send_file(file):
        with open(file, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024)  # 每次读取20M
                if not data:
                    break
                yield data
    response = StreamingHttpResponse(send_file(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response
