"""
    #  @ModuleName: AlgoMessage
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/7 12:22
"""
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from ..common.sdk_function import grep_opencv_version
from ..serializers.serializers import AlgoOpencvVersionSerializers

logger = logging.getLogger(__name__)


class AlgoOpencvVersion(APIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data
        obj = AlgoOpencvVersionSerializers(data=data)
        if not obj.is_valid():
            logging.exception(obj)
            return Response({"87": "参数错误"})
        image_name = obj.data.get('image_name')
        # 运行镜像 获取算法相关信息
        status, open_cv_version = grep_opencv_version(image_name)
        if not status:
            logging.exception(open_cv_version)
            return Response({"code": "90", "msg": open_cv_version})
        return Response(open_cv_version)
