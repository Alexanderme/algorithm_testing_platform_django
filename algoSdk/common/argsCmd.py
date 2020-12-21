"""
    #  @ModuleName: sdkCmds
    #  @Function: 算法启动命令
    #  @Author: Ljx
    #  @Time: 2020/12/3 17:19
"""

# 本次封装就不用挂载方式 使用dockerfile
import os

run_algo_cmd = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm "

url_image = "http://127.0.0.1:%s/api/analysisImage"
url_video = "http://127.0.0.1:%s/api/analysisVideo"

ias_api = "http://127.0.0.1:8000/api/sdk/iasPackage"
opencv_version = "http://127.0.0.1:8000/api/sdk/algoMessage"

algo_sdk_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建临时存放运行文件文件夹 和 算法运行结果文件夹
ori_files_dir = os.path.join(algo_sdk_dir, f"files/algoFilesdir/ori_%s")
res_files_dir = os.path.join(algo_sdk_dir, f"files/algoFileResdir/res_%s")

ias_4_url = "https://ias-1256261446.cos.ap-guangzhou.myqcloud.com/ias_v4.74_cv4.1.tar.gz"
ias_3_url = "https://ias-1256261446.cos.ap-guangzhou.myqcloud.com/ias_v4.90_cv3.4.tar.gz"
ias_4_name = "ias_v4.74_cv4.1.tar.gz"
ias_3_name = "ias_v4.90_cv3.4.tar.gz"
dockerfile_ias = os.path.join(algo_sdk_dir, "utils/sdkPackage/Dockerfile_ias")

vas_4_url = "https://vas-1256261446.cos.ap-guangzhou.myqcloud.com/vas_v4.3_cv4.1.tar.gz"
vas_3_url = "https://vas-1256261446.cos.ap-guangzhou.myqcloud.com/vas_v4.3_cv3.4.tar.gz"
vas_4_name = "vas_v4.3_cv4.1.tar.gz "
vas_3_name = "vas_v4.3_cv3.4.tar.gz"
dockerfile_vas = os.path.join(algo_sdk_dir, "utils/sdkPackage/Dockerfile_vas")

# image_build_name, image_name, package_name, package_url, dockerfile_name
docker_build_dockerfile = "docker build -t %s --build-arg IMAGE_NAME=%s --build-arg PACKAGE_NAME=%s --build-arg PACKAGE_URL=%s -f %s ."

docker_run_cmd = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm %s"
authorization_sdk_file = os.path.join(algo_sdk_dir, "utils/sdkAuthorization/give_license_sdk.sh")

docker_run_cmd_ias = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm -p %s:80 %s"

authorization_ias_file = os.path.join(algo_sdk_dir, "utils/sdkAuthorization/give_license_ias.sh")

authorization_vas_file = os.path.join(algo_sdk_dir, "utils/sdkAuthorization/give_license_vas.sh")
run_vas_file = os.path.join(algo_sdk_dir, "utils/sdkAuthorization/run.conf")

# opencv
grep_opencv = "docker exec %s bash -c \"ldd /usr/local/ev_sdk/lib/libji.so|grep 'opencv.*%s\.[0-9]'|awk 'END{print $1}'\""

sdk_privateKey = "docker exec -it  %s  bash  -c 'cat /usr/local/ev_sdk/authorization/privateKey.pem'"
auth_message = "docker exec -it  %s  bash  -c 'cat /usr/local/ev_sdk/3rd/license/lib/pkgconfig/ji_license.pc |grep -i version'"
algo_config = "docker exec -it  %s  bash  -c 'cat /usr/local/ev_sdk/config/algo_config.json'"

# 要移动的路径
res_xml_path = os.path.join(algo_sdk_dir, "utils/sdk_precision/input/ground-truth")
# 要移动的结果路径
res_txt_path = os.path.join(algo_sdk_dir, 'utils/sdk_precision/input/detection-results')
ori_json = os.path.join(algo_sdk_dir, 'utils/sdk_precision/input/.temp_files')

