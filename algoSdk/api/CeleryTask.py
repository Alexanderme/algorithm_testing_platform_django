"""
    #  @ModuleName: CeleryTask
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/15 10:21
"""
import logging
from rest_framework.response import Response
from ..serializers.serializers import CeleryTaskSerializer, FilesResultSerializer, CleanEnvSerializer
from rest_framework.views import APIView
from algoSdk.tasks import algo_ias_files
from ..common.upload_download_file import download_file
from ..common.sdk_function import clean_env

logger = logging.getLogger(__name__)

class TaskStatus(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = CeleryTaskSerializer(data=data)
        # 根据taskid 获取任务状态
        if not obj.is_valid():
            logging.exception(obj)
            return Response({"87": "参数错误"})
        task_id = obj.data.get("task_id")
        try:
            task = algo_ias_files.AsyncResult(task_id)
        except Exception as e:
            logging.exception(e)
            return Response({"code": 95, "msg": "celery执行失败"})
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
                response['error_files'] = task.info['error_files']
                response['ori_files_dir'] = task.info['ori_files_dir']
                response['res_files_dir'] = task.info['res_files_dir']
                response['container_id'] = task.info['container_id']

        else:
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),
            }
        return Response(response)


class FilesResult(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = FilesResultSerializer(data=data)
        if not obj.is_valid():
            logging.exception(obj)
            return Response({"87": "参数错误"})
        files = obj.data.get("files")
        try:
            response = download_file(files)
        except Exception as e:
            logging.exception(e)
            return Response({"code": 90, "msg": "文件下载失败"})
        return response


class CleanEvn(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = CleanEnvSerializer(data=data)
        if not obj.is_valid():
            logging.exception(obj)
            return Response({"87": "参数错误"})
        container_id = obj.data.get("container_id")
        ori_files_dir = obj.data.get("ori_files_dir")
        res_files_dir = obj.data.get("res_files_dir")
        try:
            clean_env(container_id, ori_files_dir, res_files_dir)
        except Exception as e:
            logging.exception(e)
            return Response({"code": 97, "msg": "清理运行结果失败"})
        return Response({"code": 100, "msg": "环境清理成功"})

