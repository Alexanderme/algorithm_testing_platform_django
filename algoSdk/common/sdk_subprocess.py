"""
    #  @ModuleName: sdk_subprocess
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/3 17:39
"""

import subprocess

def sdk_subprocess(cmd):
    """
    封装 subprocess 用来定制化返回消息
    :param cmd:
    :param msg:
    :return:
    """
    res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = res_p.communicate()
    returncode = res_p.returncode
    if returncode == 0:
        if stdout.endswith('\n'):
            return True, stdout.replace('\n', '')
        return True, stdout
    else:
        return False, stderr
