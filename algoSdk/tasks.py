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
import time
from .common.sdk_subprocess import sdk_subprocess
from algoSdk.common.iter_files import iter_files
from .common.sdk_function import clear_dirs, xml_create, txt_create
from .common.argsCmd import url_image, url_video, algo_sdk_dir, ori_files_dir, res_files_dir

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
    res_dir = res_files_dir % random_str
    ori_dir = ori_files_dir % random_str
    if not os.path.exists(ori_dir) or not os.path.exists(res_dir):
        try:
            os.makedirs(res_dir)
            os.makedirs(ori_dir)
        except Exception as e:
            logging.error(e)
            return False
    try:
        # 解压文件 删除下载文件
        os.system(f"unzip {file_name} -d {ori_dir}")
        os.system(f"rm -f {file_name}")
    except Exception as e:
        logging.error(e)
        return False
    # 返回文件列表
    filesname = iter_files(ori_dir, file_type="algoRunRes")
    # 获取文件全路径列表
    files_with_dir = filesname["files"]
    err_files = filesname["err_file"]
    # 计算有效文件数目
    file_nums = len(files_with_dir) - len(err_files)
    # 初始化运行文件数目
    res_files_count = 0
    cmd = f"netstat -aptn |grep {port}"
    status, res = sdk_subprocess(cmd)
    if not status:
        logging.error(status)
        return False
    # 需要判断端口是否启动成功之后才能继续往下调用算法, 不然算法没有启动车就就会导致算法运行失败
    while "LISTEN" not in res:
        status, res = sdk_subprocess(cmd)
    time.sleep(2)
    for file_with_dir in files_with_dir:
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
                res_base64 = requests.post(url_video % port, files=data).json()
            else:
                data = {
                    'image': (file, open(file_with_dir, 'rb')),
                    "args": args
                }
                res_base64 = requests.post(url_image % port, files=data).json()
        except Exception as e:
            logging.exception(e)
            return {'current': 100, 'total': 100, 'status': '算法调用失败', 'result': "-1", "error_files": err_files,
                    "ori_files_dir": ori_dir, "res_files_dir": res_dir, "container_id": container_id}
        res = res_base64.get('buffer')
        if res_base64.get("code") != 0:
            logging.exception(res)
            return {'current': 100, 'total': 100, 'status': '算法调用结果异常', 'result': "-1", "error_files": err_files,
                    "ori_files_dir": ori_dir, "res_files_dir": res_dir, "container_id": container_id}
        try:
            algo_res_json = res_base64.get("result")
        except Exception as e:
            logging.exception(e)
            return {'current': 100, 'total': 100, 'status': '获取算法json结果失败', 'result': "-1",
                    "error_files": err_files,
                    "ori_files_dir": ori_dir, "res_files_dir": res_dir, "container_id": container_id}
        res = base64.decodebytes(res.encode('ascii'))
        with open(res_file_name, 'wb') as f:
            f.write(res)
        res_file_name = res_file_name.split('/')[-1]
        with open(res_file_dir_txt, 'a') as f:
            f.write(str(res_file_name) + '\n')
            f.write(str(algo_res_json) + '\n')
        res_files_count += 1
        process = int((res_files_count / file_nums) * 100)
    algo_ias_files.update_state(state='PROGRESS', meta={'current': res_files_count, 'total': file_nums, 'status': process})
    try:
        os.system(f"cd {res_dir};tar -cvf result.tar *")
        store_path = f"{res_dir}/result.tar"
    except Exception as e:
        logging.error(e)
        return False
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': store_path, "error_files": err_files,
            "ori_files_dir": ori_dir, "res_files_dir": res_dir, "container_id": container_id}


@shared_task
def run_files(ori_files_dir, port, tag_names, iou, args, alert_info):
    clear_dirs()
    filenames = iter_files(ori_files_dir,  file_type="algoPerssion")
    xmls = filenames["xmls"]
    files = filenames["files"]
    total_files = len(files)
    file_count = 0
    cmd = f"netstat -aptn |grep {port}"
    status, res = sdk_subprocess(cmd)
    if not status:
        logging.error(status)
        return False
    time.sleep(5)
    for xml in xmls:
        xml_create(xml)
    for file in files:
        file_count += 1
        txt_create(file, port, tag_names, args, alert_info)
        process = int(file_count / total_files * 100)
        run_files.update_state(state='PROGRESS', meta={'current': file_count, 'total': total_files, 'status': process})
    main = os.path.join(algo_sdk_dir, "utils/sdk_precision/main.py")
    if iou is None:
        cmd = f"python3 {main}"
    else:
        cmd = f"python3 {main} -t {iou}"
    os.system(cmd)

    file_res = os.path.join(algo_sdk_dir, f"utils/sdk_precision/output/output.txt")
    with open(file_res, 'r') as f:
        res = f.read().splitlines()
        res = str(res).replace("'',", "\n")
    clear_dirs()
    contain_stop = "docker ps |grep %s|awk '{print $1}'|xargs docker stop" % port
    status, _ = sdk_subprocess(contain_stop)
    os.system(f"rm -rf {ori_files_dir}")
    return {'current': 100, 'total': 100, 'status': 'Task completed!', "result": res}
