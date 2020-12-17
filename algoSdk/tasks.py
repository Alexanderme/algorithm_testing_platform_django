"""
    #  @ModuleName: task
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/9 20:32
"""
import base64
import uuid
from celery import shared_task
import logging
import requests
import os

from algoSdk.common.iter_files import iter_files

logger = logging.getLogger(__name__)

@shared_task
def algo_ias_files(container_id, file_name, port, args):
    """
    后台进行 ias 运行算法得到结果
    :param args:
    :param random_str:
    :param ori_files_dir: 数据集目录
    :param self: 更新自己获取当前状态
    :param res_files_dir: 数据集运行结果目录
    :param file_name: 文件名称
    :param port: 端口
    :return:
    """
    random_str = ''.join([each for each in str(uuid.uuid1()).split('-')])
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # 创建临时存放运行文件文件夹 和 算法运行结果文件夹
    ori_files_dir = os.path.join(parent_dir, f"files/algoFilesdir/ori_{random_str}")
    res_files_dir = os.path.join(parent_dir, f"files/algoFileResdir/res_{random_str}")
    if not os.path.exists(ori_files_dir) or not os.path.exists(res_files_dir):
        try:
            os.makedirs(ori_files_dir)
            os.makedirs(res_files_dir)
        except Exception as e:
            logging.error(e)
            return False
    try:
        # 解压文件 删除下载文件
        os.system(f"unzip {file_name} -d {ori_files_dir}")
        os.system(f"rm -f {file_name}")
    except Exception as e:
        logging.error(e)
        return False
    # 返回文件列表
    filesname = iter_files(ori_files_dir, file_type="algoRunRes")
    # 获取文件全路径列表
    files_with_dir = filesname["files"]
    err_files = filesname["err_file"]
    # 计算有效文件数目
    file_nums = len(files_with_dir) - len(err_files)
    # 初始化运行文件数目
    res_files_count = 0
    try:
        process = run_files(files_with_dir, random_str,  port, ori_files_dir, res_files_dir, err_files, container_id, res_files_count, file_nums, args)
    except Exception as e:
        logging.exception(e)
        return False
    logging.info(process)
    algo_ias_files.update_state(state='PROGRESS', meta={'current': res_files_count, 'total': file_nums, 'status': process})
    # 打包
    try:
        os.system(f"cd {res_files_dir};tar -cvf result.tar *")
        store_path = f"{res_files_dir}/result.tar"
    except Exception as e:
        logging.error(e)
        return False

    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': store_path, "error_files": err_files,
            "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}


def run_files(files, random_str, port, ori_files_dir, res_files_dir, err_files, container_id, res_files_count, file_nums, args):
    url_image = "http://127.0.0.1" + ":" + str(port) + "/api/analysisImage"
    url_video = "http://127.0.0.1" + ":" + str(port) + "/api/analysisVideo"
    for file_with_dir in files:
        # 原文件名称 文件路径
        file_dir, file = os.path.split(file_with_dir)
        # 结果文件路径
        res_file_dir = file_dir.replace(f"ori_{random_str}", f"res_{random_str}").replace("algoFilesdir", "algoFileResdir")
        res_file_dir_txt = os.path.join(res_file_dir, "res.txt")
        res_file_name = os.path.join(res_file_dir, file)
        # 调用IAS
        try:
            if file.lower().endswith("avi") or file.lower().endswith("mp4") or file.lower().endswith("flv"):
                data = {
                    'video': (file, open(file_with_dir, 'rb')),
                    "args": args
                }
                res_base64 = requests.post(url_video, files=data).json()
                print("----------------------------------")
            else:
                data = {
                    'image': (file, open(file_with_dir, 'rb')),
                    "args": args
                }
                res_base64 = requests.post(url_image, files=data).json()
                print("----------------------------------")
        except Exception as e:
            logging.exception(e)
            return {'current': 100, 'total': 100, 'status': '算法调用失败', 'result': "-1", "error_files": err_files,
                    "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        res = res_base64.get('buffer')
        if res_base64.get("code") != 0:
            logging.exception(res)
            return {'current': 100, 'total': 100, 'status': '算法调用结果异常', 'result': "-1", "error_files": err_files,
                    "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        try:
            algo_res_json = res_base64.get("result")
        except Exception as e:
            logging.exception(e)
            return {'current': 100, 'total': 100, 'status': '获取算法json结果失败', 'result': "-1", "error_files": err_files,
                    "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        res = base64.decodebytes(res.encode('ascii'))
        with open(res_file_name, 'wb') as f:
            f.write(res)
        res_file_name = res_file_name.split('/')[-1]
        with open(res_file_dir_txt, 'a') as f:
            f.write(str(res_file_name) + '\n')
            f.write(str(algo_res_json) + '\n')
        res_files_count += 1
        process = int((res_files_count / file_nums) * 100)
        return process