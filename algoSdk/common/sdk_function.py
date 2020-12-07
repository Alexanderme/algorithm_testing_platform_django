"""
    #  @ModuleName: sdk_function
    #  @Function: 用于存放该APP下面共用相同的函数方法
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:38
"""

from .sdk_subprocess import sdk_subprocess
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""

svas   https://vas-1256261446.cos.ap-guangzhou.myqcloud.com
svas_v1.0cv3.4.tar.gz
svas_v1.0cv4.1.tar.gz
"""


def docker_build(image_build_name, dockerfile_name, image_name, package_name, package_url ):
    """
    用于dockerfile来创建封装好的vas, ias镜像
    :param image_build_name: 封装后的镜像名称
    :param dockerfile_name: dockerfile文件
    :return:
    """
    docker_build = f"docker build -t {image_build_name} --build-arg IMAGE_NAME={image_name} " \
                   f"--build-arg PACKAGE_NAME={package_name} --build-arg PACKAGE_URL={package_url} -f {dockerfile_name} ."
    status, _ = sdk_subprocess(docker_build)
    if not status:
        return False
    return status



def docker_run_ias(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:80 {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        return False, res
    contain_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdkAuthorization/give_license_ias.sh")
    docker_authorization = f"docker cp {authorization_file} {contain_id}:/root"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        return False, res
    ias_install = f"docker exec  {contain_id} bash /root/give_license_ias.sh"
    status, res = sdk_subprocess(ias_install)
    if not status:
        return False, res
    return True, "sucess"



def docker_run_vas(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:10000 {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        return False, res
    contain_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdkAuthorization/give_license_vas.sh")
    docker_authorization = f"docker cp {authorization_file} {contain_id}:/root"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        return False, res
    # 负责运行文件到容器
    run_file = os.path.join(path, "utils/sdkAuthorization/run.conf")
    docker_authorization = f"docker cp {run_file} {contain_id}:/usr/local/vas"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        return False, res
    ias_install = f"docker exec  {contain_id} bash /root/give_license_vas.sh"
    status, res = sdk_subprocess(ias_install)
    if not status:
        return False, res
    return True, "sucess"

