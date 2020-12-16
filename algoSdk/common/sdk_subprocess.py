"""
    #  @ModuleName: sdk_subprocess
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/3 17:39
"""

import subprocess
import logging

logger = logging.getLogger(__name__)

def sdk_subprocess(cmd):
    """
    封装 subprocess 用来定制化返回消息
    :param cmd: 运行命令
    :return: 返回命令运行结果以及状态码
    """
    try:
        res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = res_p.communicate()
    except Exception as e:
        logging.exception(e)
        # 部分镜像不兼容utf-8 报错使用如下格式
        res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 encoding='unicode_escape')
        stdout, stderr = res_p.communicate()
    if res_p.returncode == 0:
        if stdout.endswith('\n'):
            return True, stdout.replace('\n', '')
        return True, stdout
    else:
        logging.exception(stderr)
        return False, stderr
