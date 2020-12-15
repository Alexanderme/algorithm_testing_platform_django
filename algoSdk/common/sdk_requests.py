"""
    #  @ModuleName: sdk_requests
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/11 15:04
"""
import requests

ias_api = "http://127.0.0.1:8000/api/sdk/iasPackage"
opencv_version = "http://127.0.0.1:8000/api/sdk/algoMessage"

def ias_packing(port, image_name, version):
    data = {
        "port": port,
        "image_name": image_name,
        "version": version
    }
    res = requests.post(ias_api, data=data).json()
    code = res.get("code")
    if code != "100":
        return False
    container_id = res.get("container_id")
    return True, container_id


def get_sdk_opencv_version(image_name):
    data = {
        "image_name": image_name
    }
    res = requests.post(opencv_version, data=data).json().get("code")
    if res != "100":
        return False
    else:
        return requests.post(opencv_version, data=data).json().get("OpenCV_version")