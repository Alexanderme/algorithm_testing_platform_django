"""
    #  @ModuleName: AlgoRunRes
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/8 20:35
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from ..celery_tasks.algo_res_task import algo_ias_files
from ..serializers.serializers import AlgoResSerializer
from ..common.upload_download_file import upload_file
from dj_extremevision.settings import Algo_files_Res_dir, Algo_files_dir
from ..common.sdk_requests import ias_packing, get_sdk_opencv_version
import random

class AlgoRes(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = AlgoResSerializer(data=data)
        if not obj.is_valid():
            return Response({"87": "参数错误"})
        image_name = obj.data.get('image_name')
        args = obj.data.get('args')
        # 保存文件
        status, file_name = upload_file(requests, Algo_files_dir)
        if not status:
            return Response({"code": "96", "msg": "文件上传失败"})
        opencv_version = get_sdk_opencv_version(image_name)
        if not opencv_version:
            return Response({"code": "98", "msg": "获取算法opencv版本失败"})
        else:
            opencv_version = int(opencv_version)
        port = random.randint(30000, 60000)
        status, container_id = ias_packing(port, image_name, opencv_version)
        if not status:
            return Response({"code": "92", "msg": "封装ias失败"})

        task = algo_ias_files(container_id, Algo_files_dir, Algo_files_Res_dir, file_name, port, args)

        return Response({"code": "96", "msg": "文件上传失败", "task_id": task.id})


