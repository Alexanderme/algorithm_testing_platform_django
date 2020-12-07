"""
    #  @ModuleName: sdkCmds
    #  @Function: 算法启动命令
    #  @Author: Ljx
    #  @Time: 2020/12/3 17:19
"""

# 本次封装就不用挂载方式 使用dockerfile

run_algo_cmd = "docker run -itd --runtime=nvidia --privileged   -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm "




