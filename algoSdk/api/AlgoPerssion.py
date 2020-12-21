"""
    #  @ModuleName: AlgoPerssion
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/18 16:49
"""
import os
import random
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from ..common.sdk_requests import ias_packing, get_sdk_opencv_version
from ..serializers.serializers import GetFilesResultSerializer
import logging
from ..tasks import run_files
from ..common.upload_download_file import upload_file
from dj_extremevision.settings import Algo_files_dir
from ..common.argsCmd import ori_files_dir

logger = logging.getLogger(__name__)



class GetFilesResult(APIView):
    """
    需要用户指定服务器中的图片,xml存放的路径  指定算法标签  报警字段默认alert_info="alert_info"
    :return:
    """
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = GetFilesResultSerializer(data=data)
        if not obj.is_valid():
            logging.exception(obj)
            return Response({"87": "参数错误"})
        image_name = obj.data.get('image_name')
        args = obj.data.get('args')
        tag_names = obj.data.get('tag_names')
        alert_info = obj.data.get('alert_info')
        iou = obj.data.get('iou')
        tag_names = tag_names.replace(" ", "").split(",")
        status, file_name = upload_file(requests, Algo_files_dir)
        if not status:
            logging.exception(file_name)
            return Response({"code": "96", "msg": "文件上传失败"})

        random_str = ''.join([each for each in str(uuid.uuid1()).split('-')])
        # 创建临时存放运行文件文件夹 和 算法运行结果文件夹
        ori_dir = ori_files_dir % random_str
        os.system(f"unzip {file_name} -d {ori_dir}")
        os.system(f"rm -rf {file_name}")

        opencv_version = get_sdk_opencv_version(image_name)
        if not opencv_version:
            logging.exception(opencv_version)
            return Response({"code": "90", "msg": "获取算法opencv版本失败"})
        else:
            opencv_version = float(opencv_version)
        port = random.randint(30000, 60000)
        status, container_id = ias_packing(port, image_name, opencv_version)
        if not status:
            logging.exception(container_id)
            return Response({"code": "90", "msg": "封装ias失败"})

        task = run_files.delay(ori_dir, port, tag_names, iou, args, alert_info)

        return Response({"code": "100", "msg": "celery任务启动成功", "task_id": task.id})