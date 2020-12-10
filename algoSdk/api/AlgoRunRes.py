"""
    #  @ModuleName: AlgoRunRes
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/8 20:35
"""
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.serializers import AlgoResSerializer
from ..common.upload_download_file import upload_file
from dj_extremevision.settings import Algo_Res_dir


class AlgoRes(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = AlgoResSerializer(data=data)
        if not obj.is_valid():
            return Response({"87": "参数错误"})
        image_name = obj.data.get('image_name')
        args = obj.data.get('args')
        file_name = obj.data.get('file_name')
        # 保存文件
        status = upload_file(requests, file_name, Algo_Res_dir)
        if not status:
            return Response({"96": "文件上传失败"})
        return Response({"100": "文件上传成功"})