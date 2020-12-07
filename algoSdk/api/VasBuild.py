"""
    #  @ModuleName: VasBuild
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/7 11:41
"""

"""
    #  @ModuleName: IasBuild
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:32
"""
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializers import VasPackageSerializers
from ..common.sdk_function import docker_build
from ..common.sdk_function import docker_run_vas

import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


vas_4_url = "https://vas-1256261446.cos.ap-guangzhou.myqcloud.com/vas_v4.3_cv4.1.tar.gz"
vas_3_url = "https://vas-1256261446.cos.ap-guangzhou.myqcloud.com/vas_v4.3_cv3.4.tar.gz"
vas_4_name = "vas_v4.3_cv4.1.tar.gz "
vas_3_name = "vas_v4.3_cv3.4.tar.gz"


class VasPackage(APIView):
    """
    用于封装Vas
    """
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = VasPackageSerializers(data=data)
        if not obj.is_valid():
            return Response({"87": "参数错误"})
        image_name = obj.data.get("image_name")
        port = obj.data.get("port")
        version = obj.data.get("version")
        dockerfile_vas = os.path.join(path, "utils/sdkPackage/Dockerfile_vas")
        image = image_name + "_test_vas"
        # 封装镜像
        if version == "3.4":
            status = docker_build(image, dockerfile_vas, image_name, vas_3_name, vas_3_url)
            if not status:
                return Response({"code": "91", "msg": "dockerfile生成失败"})
        else:
            status = docker_build(image, dockerfile_vas, image_name, vas_4_name, vas_4_url)
            if not status:
                return Response({"code": "91", "msg": "dockerfile生成失败"})
        # 运行镜像
        status, res = docker_run_vas(image, port)
        if not status:
            if "port is already" in res:
                return Response({"code": "92", "msg": "算法启动失败, 端口被占用"})
            else:
                return Response({"code": "92", "msg": "算法启动失败, 请确保镜像存在或者镜像名称正确"})
        return Response({"code": "100", "msg": "封装VAS成功,可以直接调用VAS"})
