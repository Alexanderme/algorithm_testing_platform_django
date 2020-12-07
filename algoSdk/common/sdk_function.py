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
vas:  https://vas-1256261446.cos.ap-guangzhou.myqcloud.com
vas_v4.1_cv3.4.tar.gz        
vas_v4.1_cv4.1.tar.gz        
vas_v4.2_cv4.1.tar.gz
vas_v4.3_cv4.1.tar.gz 
vas_v4.3_cv3.4.tar.gz

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
                   f"--build-arg package_name={package_name} --build-arg package_url={package_url} -f {dockerfile_name}/Dockerfile ."
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
        return False, res
    contain_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdk_authorization/give_license.sh")
    f"docker cp {authorization_file} {contain_id}:/root"
    ias_install = f"docker exec  {contain_id} bash /root/give_license.sh &"
    status, res = sdk_subprocess(ias_install)
    print(res)
    if not status:
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
