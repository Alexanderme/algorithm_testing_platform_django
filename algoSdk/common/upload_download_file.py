"""
    #  @ModuleName: upload_download_file
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/10 19:56
"""
import os


def upload_file(obj, save_dir):
    """
    用于处理上传文件
    :return:
    """
    File = obj.data.get('file_name')
    file_dir = os.path.join(save_dir, File.name)
    if File is None:
        return False
    else:
        with open(file_dir, 'wb+') as f:
            for chunk in File.chunks():
                f.write(chunk)
        return True


def download_file(files):
    """
    用于处理下载文件
    :return:
    """
    with open(files, 'rb') as targetfile:
        while 1:
            data = targetfile.read(20 * 1024)  # 每次读取20M
            if not data:
                break
            yield data
    return True

# def download_file(file):
#     """
#     用于处理下载文件
#     :return:
#     """
#     def send_file(files):
#         with open(files, 'rb') as targetfile:
#             while 1:
#                 data = targetfile.read(20 * 1024)  # 每次读取20M
#                 if not data:
#                     break
#                 yield data
#     response = StreamingHttpResponse(send_file(file))
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
#     return response
