"""
    #  @ModuleName: sdk_function
    #  @Function: 用于存放该APP下面共用相同的函数方法
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:38
"""

from .sdk_subprocess import sdk_subprocess
from rest_framework.response import Response


def docker_build(image_build_name, dockerfile_name):
    """
    用于dockerfile来创建封装好的vas, ias镜像
    :param image_build_name: 封装后的镜像名称
    :param dockerfile_name: dockerfile文件
    :return:
    """
    docker_build = "docker build -f %s -t %s ." % (dockerfile_name, image_build_name)
    status, _ = sdk_subprocess(docker_build)
    if not status:
        return False



def docker_run_ias(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:80 {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        # return Response({"code": "92", "msg": "算法启动失败"})
        return False, res



def docker_run_vas(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:10000 {image_name}"

    status, res = sdk_subprocess(docker_run)
    if not status:
        # return Response({"code": "92", "msg": "算法启动失败"})
        return False, res
