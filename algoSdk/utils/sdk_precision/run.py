from bs4 import BeautifulSoup
import os
import requests
import shutil
from collections import defaultdict
from extremevision import celery
from extremevision.api_1_0.sdk_subprocess import sdk_subprocess
import time
import base64
from extremevision.sdk_config import request_host_without_port


BASE_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
RES_DIR = os.path.abspath(os.path.join(os.path.abspath(BASE_DIR), "input"))

# 要移动的路径
res_xml_path = os.path.join(RES_DIR, "ground-truth")
# 要移动的结果路径
res_txt_path = os.path.join(RES_DIR, 'detection-results')
ori_json = os.path.join(BASE_DIR, '.temp_files')


def clear_dirs():
    # 先清空文件夹 在创建文件夹
    if os.path.exists(RES_DIR):
        shutil.rmtree(RES_DIR)
    if os.path.exists(ori_json):
        shutil.rmtree(ori_json)
    # 创建需要的文件夹
    os.mkdir(RES_DIR)
    detection_results = os.path.join(RES_DIR, "detection-results")
    ground_truth = os.path.join(RES_DIR, "ground-truth")
    files = os.path.join(RES_DIR, "files")
    os.makedirs(detection_results)
    os.makedirs(ground_truth)
    os.makedirs(files)

@celery.task(bind=True)
def run_files(self, rootDir, port, names, iou, args, alert_info, hat):
    filenames = iter_files(rootDir)
    xmls = filenames["xmls"]
    files = filenames["files"]
    total_files = len(files)
    file_count = 0
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for xml in xmls:
        xml_create(xml, path)
    time.sleep(3)
    for file in files:
        file_count += 1
        if hat is not None and hat.endswith("gpu"):
            hat = "report_num_hat"
            txt_create(file, port, names, args, alert_info, hat)
        else:
            txt_create(file, port, names, args, alert_info)    
        process = int(file_count/total_files*100)
        self.update_state(state='PROGRESS', meta={'current': file_count, 'total': total_files, 'status': process})
    main = os.path.join(path, "utils/sdk_precision/main.py")
    if iou is None:
        cmd = f"python3 {main}"
    else:
        cmd = f"python3 {main} -t {iou}"
    os.system(cmd)
    
    file_res = os.path.join(path, f"utils/sdk_precision/output/output.txt")
    with open(file_res, 'r') as f:
        res = f.read().splitlines()
        res = str(res).replace("'',", "\n")
    clear_dirs()
    contain_stop = "docker ps |grep %s|awk '{print $1}'|xargs docker stop" % port
    status, _ = sdk_subprocess(contain_stop)
    print(rootDir, "rootDir")
    os.system(f"rm -rf {rootDir}")
    return {'current': 100, 'total': 100, 'status': 'Task completed!', "result": res}

def iter_files(rootDir):
    """
    根据文件路径 返回文件名称 以及文件路径名称
    :param rootDir:
    :return:
    """
    filenames = defaultdict(list)
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file = os.path.join(root, file)
            if file.lower().endswith('xml'):
                filenames["xmls"].append(file)
            if file.lower().endswith('jpg') or file.lower().endswith('png'):
                filenames["files"].append(file)
        for dir in dirs:
            iter_files(dir)

    return filenames


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


def txt_create(file, port, names, args, alert_info, hat=None):
    url = request_host_without_port + ":" + str(port) + "/api/analysisImage"
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
            if res.get(name) is not None:
                if hat is not None:
                    name = "report_num_hat"
                    name = res.get(name)
                    if int(name) == 1:
                        name = "hat"
                    else:
                        name = "head"
                else:
                    name = res.get(name)
                x = res.get('x')
                y = res.get('y')
                width = res.get('width') + x
                height = res.get('height') + y
                with open(os.path.join(res_txt_path, name_txt), "a") as f:
                    f.write("%s %s %s %s %s %s\n" % (name, confidence, x, y, width, height))
            else:
                x = res.get('x')
                y = res.get('y')
                width = res.get('width') + x
                height = res.get('height') + y
                with open(os.path.join(res_txt_path, name_txt), "a") as f:
                    f.write("%s %s %s %s %s %s\n" % (name, confidence, x, y, width, height))
