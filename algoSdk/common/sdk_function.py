"""
    #  @ModuleName: sdk_function
    #  @Function: 用于存放该APP下面共用相同的函数方法
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:38
"""
import requests

from .sdk_subprocess import sdk_subprocess
import subprocess
import re
import os
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""

svas   https://vas-1256261446.cos.ap-guangzhou.myqcloud.com
svas_v1.0cv3.4.tar.gz
svas_v1.0cv4.1.tar.gz
"""


def docker_build(image_build_name, dockerfile_name, image_name, package_name, package_url):
    """
    用于dockerfile来创建封装好的vas, ias镜像
    :param image_build_name: 封装后的镜像名称
    :param dockerfile_name: dockerfile文件
    :return:
    """
    docker_build = f"docker build -t {image_build_name} --build-arg IMAGE_NAME={image_name} " \
                   f"--build-arg PACKAGE_NAME={package_name} --build-arg PACKAGE_URL={package_url} -f {dockerfile_name} ."
    status, res = sdk_subprocess(docker_build)
    if not status:
        logging.exception(res)
        return False
    return status


def docker_run_sdk(image_name):
    docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                 f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        logging.exception(res)
        return False, res
    container_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdkAuthorization/give_license_sdk.sh")
    docker_authorization = f"docker cp {authorization_file} {container_id}:/root"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        logging.exception(res)
        return False, res
    ias_install = f"docker exec  {container_id} bash /root/give_license_sdk.sh"
    status, res = sdk_subprocess(ias_install)
    if not status:
        logging.exception(res)
        return False, res
    return True, container_id


def docker_run_ias(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:80 {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        logging.exception(res)
        return False, res
    container_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdkAuthorization/give_license_ias.sh")
    docker_authorization = f"docker cp {authorization_file} {container_id}:/root"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        logging.exception(res)
        return False, res
    ias_install = f"docker exec  {container_id} bash /root/give_license_ias.sh &"
    # 因为存在等待信息返回的一个状态 ,部分服务器会一直等待请求返回结果  先用上面的尝试
    status, res = sdk_subprocess(ias_install)
    if not status:
        logging.exception(res)
        return False, res
    return True, container_id


def docker_run_vas(image_name, port=None):
    if port is None:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm {image_name}"
    else:
        docker_run = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e " \
                     f"NVIDIA_VISIBLE_DEVICES=0 --rm -p {port}:10000 {image_name}"
    status, res = sdk_subprocess(docker_run)
    if not status:
        logging.exception(res)
        return False, res
    container_id = res[:12]
    # 复制授权文件到容器
    authorization_file = os.path.join(path, "utils/sdkAuthorization/give_license_vas.sh")
    docker_authorization = f"docker cp {authorization_file} {container_id}:/root"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        logging.exception(res)
        return False, res
    # 负责运行文件到容器
    run_file = os.path.join(path, "utils/sdkAuthorization/run.conf")
    docker_authorization = f"docker cp {run_file} {container_id}:/usr/local/vas"
    status, res = sdk_subprocess(docker_authorization)
    if not status:
        logging.exception(res)
        return False, res
    vas_install = f"docker exec  {container_id} bash /root/give_license_vas.sh "
    os.popen(vas_install)
    return True, container_id


def grep_opencv_version(image):
    errmsg = {}
    status, container_id = docker_run_sdk(image)
    if not status:
        logging.exception(container_id)
        return False, "sdk算法启动失败"
    grep_opencv = f"docker exec {container_id} bash -c \"ldd /usr/local/ev_sdk/lib/libji.so|" \
                  "grep 'opencv.*3\.[0-9]'|awk 'END{print $1}'\""
    status, opencv_version = sdk_subprocess(grep_opencv)
    try:
        pattern_3 = ".*?(3.\d)"
        opencv_version = re.findall(pattern_3, opencv_version)[0]
        if not status:
            logging.exception(opencv_version)
            errmsg.update({"OpenCV_version": "获取OpenCV版本失败"})
        errmsg.update({"OpenCV_version": opencv_version})
    except Exception as e:
        logger.exception(e)
        grep_opencv = f"docker exec {container_id} bash -c \"ldd /usr/local/ev_sdk/lib/libji.so|" \
                  "grep 'opencv.*4\.[0-9]'|awk 'END{print $1}'\""
        status, opencv_version = sdk_subprocess(grep_opencv)
        if not status:
            logging.exception(opencv_version)
            errmsg.update({"OpenCV_version": "获取OpenCV版本失败"})
        pattern_4 = ".*?(4.\d)"
        opencv_version = re.findall(pattern_4, opencv_version)[0]
        errmsg.update({"OpenCV_version": opencv_version})
    sdk_message = f"docker exec -it  {container_id}  bash  -c 'cat /usr/local/ev_sdk/authorization/privateKey.pem'"
    status, res_p = sdk_subprocess(sdk_message)
    if "No such file or directory" not in res_p:
        errmsg.update({"sdk_version": "算法SDK版本为3.0系列 配置路径为:/usr/local/ev_sdk/config/algo_config.json \n"})
    else:
        logging.exception(res_p)
        return False, "算法SDK版本为2.0系列 不输出内容"

    auth_message = f"docker exec -it  {container_id}  bash  -c 'cat /usr/local/ev_sdk/3rd/license/lib/pkgconfig/ji_license.pc |grep -i version'"
    status, res = sdk_subprocess(auth_message)
    if not res.startswith("cat"):
        errmsg.update({"sdk_authorization": "当前默认应该使用最新的版本库20.1.3, 当前算法授权库版本为" + res})
    else:
        logging.exception(res)
        errmsg.update({"sdk_authorization": "获取授权信息失败, 授权库不是最新的20.1.3"})

    # 公私钥  配置文件 查看
    privateKey = f"docker exec -it  {container_id}  bash  -c 'cat /usr/local/ev_sdk/authorization/privateKey.pem'"
    status, privateKey = sdk_subprocess(privateKey)
    if not status:
        logging.exception(privateKey)
        errmsg.update({"privateKey": "获取获取失败"})
    if privateKey == "":
        errmsg.update({"Sdk_version": 2.5})
    else:
        errmsg.update({"Sdk_version": 3.0})
    errmsg.update({"privateKey": privateKey})
    algo_config = f"docker exec -it  {container_id}  bash  -c 'cat /usr/local/ev_sdk/config/algo_config.json'"
    status, algo_config = sdk_subprocess(algo_config)
    if not status:
        logging.exception(algo_config)
        errmsg.update({"algo_config": "获取获取配置失败"})
    errmsg.update({"algo_config": algo_config})
    if opencv_version.startswith("3."):
        errmsg.update({"algo_message": '当前OpenCV版本为:3.4, vas安装包:vas_v4.3_cv3.4.tar.gz, ias安装包:ias_v4.90_cv3.4.tar.gz'})
        stop = f"docker stop {container_id}"
        status, res = sdk_subprocess(stop)
        if not status:
            logging.exception(res)
            errmsg.update({"stop_container": "停用容器失败"})
    elif opencv_version.startswith("4."):
        errmsg.update({"algo_message": '当前OpenCV版本为:4.1, vas安装包:vas_v4.3_cv4.1.tar.gz, ias安装包:ias_v4.74_cv4.1.tar.gz'})
        stop = f"docker stop {container_id}"
        status, res = sdk_subprocess(stop)
        if not status:
            logging.exception(res)
            errmsg.update({"stop_container": "停用容器失败"})
    else:
        errmsg.update({"algo_message": '当前OpenCV版本为: 获取失败'})
        stop = f"docker stop {container_id}"
        status, res = sdk_subprocess(stop)
        if not status:
            logging.exception(res)
            errmsg.update({"stop_container": "停用容器失败"})
    errmsg.update({"code": "100"})
    return True, errmsg


def clean_env(*args, **kwargs):
    """
    用于清理环境, 删除图片等弃用数据
    :return:
    """
    container_id = kwargs.get("container_id")
    ori_files_dir = kwargs.get("ori_files_dir")
    res_files_dir = kwargs.get("res_files_dir")
    if not all([container_id, ori_files_dir, res_files_dir]):
       logging.exception(res_files_dir, ori_files_dir, container_id)
       return False
    # other =  kwargs.get("other")
    if container_id:
        os.system(f"docker stop {container_id}")
    # 删除 运行文件
    if ori_files_dir:
        os.system(f"rm -rf {ori_files_dir}")
    if res_files_dir:
        os.system(f"rm -rf {res_files_dir}")


BASE_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
RES_DIR = os.path.abspath(os.path.join(os.path.abspath(BASE_DIR), "input"))

# 要移动的路径
res_xml_path = os.path.join(RES_DIR, "ground-truth")
# 要移动的结果路径
res_txt_path = os.path.join(RES_DIR, 'detection-results')
ori_json = os.path.join(BASE_DIR, '.temp_files')



def xml_create(file, path):
    root = os.path.join(path, "utils/sdk_precision/input/ground-truth")
    name_txt = file.split('/')[-1].split('.')[0] + ".txt"
    print("xml_create", name_txt)
    with open(file, "rb") as f:
        file_b = f.read()
    soup = BeautifulSoup(file_b, 'lxml')
    object_all = soup.find_all("object")
    for i in object_all:
        name = i.find_all("name")[0].string
        for m in i.find_all("bndbox"):
            xmin = m.find_all("xmin")[0].string
            ymin = m.find_all("ymin")[0].string
            xmax = m.find_all("xmax")[0].string
            ymax = m.find_all("ymax")[0].string
            with open(os.path.join(root, name_txt), "a") as f:
                f.write(
                    "%s %s %s %s %s\n" % (name, int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax))))


def txt_create(file, port, names, args, alert_info):
    url = "http://127.0.0.1" + ":" + str(port) + "/api/analysisImage"
    image = file.split('/')[-1]
    data = {
        'image': (image, open(file, 'rb')),
        "args": args
    }
    response = requests.post(url, files=data)
    if alert_info is None:
        alert_info = "alert_info"
    res_index = response.json().get("result").get(alert_info)
    name_txt = file.split('/')[-1].split('.')[0] + ".txt"
    if res_index is None or res_index == [] or res_index == 'null' or res_index == 'Null' or res_index == 'NULL':
        with open(os.path.join(res_txt_path, name_txt), "a") as f:
            f.write("\n")
        return
    for res in res_index:
        if res.get('confidence') is not None:
            confidence = res.get('confidence')
        else:
            confidence = "1"
        for name in names:
            x = res.get('x')
            y = res.get('y')
            width = res.get('width') + x
            height = res.get('height') + y
            with open(os.path.join(res_txt_path, name_txt), "a") as f:
                f.write("%s %s %s %s %s %s\n" % (name, confidence, x, y, width, height))
