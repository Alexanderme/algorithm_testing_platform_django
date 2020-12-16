"""
    #  @ModuleName: IasBuild
    #  @Function:
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:32
"""
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializers import IasPackageSerializers
from ..common.sdk_function import docker_build
from ..common.sdk_function import docker_run_ias
from ..common.sdk_requests import get_sdk_opencv_version

import os
import logging

logger = logging.getLogger(__name__)

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ias_4_url = "https://ias-1256261446.cos.ap-guangzhou.myqcloud.com/ias_v4.74_cv4.1.tar.gz"
ias_3_url = "https://ias-1256261446.cos.ap-guangzhou.myqcloud.com/ias_v4.90_cv3.4.tar.gz"
ias_4_name = "ias_v4.74_cv4.1.tar.gz"
ias_3_name = "ias_v4.90_cv3.4.tar.gz"



class IasPackage(APIView):
    """
    用于封装ias
    """
    def post(self, requests, *args, **kwargs):
        data = requests.data
        serializer = IasPackageSerializers(data=data)
        if not serializer.is_valid():
            logging.exception(serializer)
            return Response({"87": "参数错误"})
        image_name = serializer.data.get("image_name")
        port = serializer.data.get("port")

        dockerfile_ias = os.path.join(path, "utils/sdkPackage/Dockerfile_ias")
        image = image_name + "_test_ias"
        opencv_version = get_sdk_opencv_version(image_name)
        if not opencv_version:
            logging.exception(opencv_version)
            return Response({"code": "90", "msg": "算法启动失败, 获取算法OpenCV失败"})
        # 封装镜像
        if opencv_version.startswith("3."):
            status = docker_build(image, dockerfile_ias, image_name, ias_3_name, ias_3_url)
            if not status:
                return Response({"code": "90", "msg": "dockerfile生成失败"})
        else:
            status = docker_build(image, dockerfile_ias, image_name, ias_4_name, ias_4_url)
            if not status:
                return Response({"code": "90", "msg": "dockerfile生成失败"})
        # 运行镜像
        status, res = docker_run_ias(image, port)
        if not status:
            if "port is already" in res:
                logging.exception(res)
                return Response({"code": "90", "msg": "算法启动失败, 端口被占用"})
            else:
                logging.exception(res)
                return Response({"code": "90", "msg": "算法启动失败, 请确保镜像存在或者镜像名称正确"})
        return Response({"code": "100", "msg": "封装IAS成功,可以直接调用IAS", "container_id": res})
