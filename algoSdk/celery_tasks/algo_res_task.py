"""
    #  @ModuleName: task
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/9 20:32
"""
from ..common.iter_files import iter_files
from celery import shared_task
from ..common.sdk_subprocess import sdk_subprocess
import os
import time



@shared_task
def algo_ias_files(ori_files_dir, res_files_dir, file_name, port, args, random_str):
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
    # 解压文件
    os.system(f"unzip {file_name} -d {ori_files_dir}")
    os.system(f"rm -f {file_name}")
    # 调用ias, image , video
    filesname = iter_files(ori_files_dir)
    # 获取文件全路径列表
    images_dir = filesname["image_dir"]
    videos_dir = filesname["video_dir"]
    err_files = filesname["err_file"]

    file_nums = len(images_dir) + len(videos_dir) - len(err_files)
    res_files_count = 0
    cmd = "docker ps|grep %s|awk '{print $1}'" % port
    status, res = sdk_subprocess(cmd)
    time.sleep(5)
    cmd = "docker ps|grep %s|awk '{print $1}'" % port
    status, container_id = sdk_subprocess(cmd)

    for image_dir in images_dir:
        url = request_host_without_port + ":" + str(port) + "/api/analysisImage"
        # 原文件名称 文件路径
        file_dir, image = os.path.split(image_dir)
        # 结果文件路径
        res_file_dir = file_dir.replace(f"ori_{random_str}", f"res_{random_str}")
        res_file_dir_txt = os.path.join(res_file_dir, "res.txt")
        if not os.path.exists(res_file_dir):
            os.makedirs(res_file_dir)
        res_file_name = os.path.join(res_file_dir, image)
        # 调用IAS
        data = {
            'image': (image, open(image_dir, 'rb')),
            "args": args
        }
        try:
            res_base64 = requests.post(url, files=data).json()
            print(res_base64.get("code")==0)
            if res_base64.get("code") != 0:
                return {'current': 100, 'total': 100, 'status': 'faild', 'result': "-1", "error_files": err_files,"ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        except Exception as e:
            res_base64 = {"code":-100}
            return {'current': 100, 'total': 100, 'status': 'faild', 'result': "-100", "error_files": err_files,
            "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        res = res_base64.get('buffer')
        algo_res_json = res_base64.get("result")
        res = base64.decodebytes(res.encode('ascii'))
        with open(res_file_name, 'wb') as f:
            f.write(res)
        res_file_name = res_file_name.split('/')[-1]
        with open(res_file_dir_txt, 'a') as f:
            f.write(str(res_file_name) + '\n')
            f.write(str(algo_res_json) + '\n')
        res_files_count += 1
        process = int((res_files_count / file_nums) * 100)
        self.update_state(state='PROGRESS', meta={'current': res_files_count, 'total': file_nums, 'status': process})

    for video_dir in videos_dir:
        url = request_host_without_port + ":" + str(port) + "/api/analysisVideo"
        # 原文件名称 文件路径
        file_dir, video = os.path.split(video_dir)
        # 结果文件路径
        res_file_dir = file_dir.replace(f"ori_{random_str}", f"res_{random_str}")
        res_file_dir_txt = os.path.join(res_file_dir, "res.txt")
        if not os.path.exists(res_file_dir):
            os.makedirs(res_file_dir)
        res_file_name = os.path.join(res_file_dir, video)
        # 调用IAS
        data = {
            'video': (video, open(video_dir, 'rb')),
            "args": args
        }
        try:
            res_base64 = requests.post(url, files=data).json()
            if res_base64.get("code") != 0:
                return {'current': 100, 'total': 100, 'status': 'faild', 'result': "-1", "error_files": err_files,"ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        except Exception as e:
            res_base64 = {"code":-100}
            return {'current': 100, 'total': 100, 'status': 'faild', 'result': "-100", "error_files": err_files,
            "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}
        res = res_base64.get('buffer')
        algo_res_json = res_base64.get("result")
        res = base64.decodebytes(res.encode('ascii'))
        with open(res_file_name, 'wb') as f:
            f.write(res)
        res_file_name = res_file_name.split('/')[-1]
        with open(res_file_dir_txt, 'a') as f:
            f.write(str(res_file_name) + '\n')
            f.write(str(algo_res_json) + '\n')
        res_files_count += 1
        process = int((res_files_count / file_nums) * 100)
        self.update_state(state='PROGRESS', meta={'current': res_files_count, 'total': file_nums, 'status': process})

    # 打包下载结果
    os.system(f"cd {res_files_dir};tar -cvf result.tar *")
    store_path = f"{res_files_dir}/result.tar"

    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': store_path, "error_files": err_files,
            "ori_files_dir": ori_files_dir, "res_files_dir": res_files_dir, "container_id": container_id}

