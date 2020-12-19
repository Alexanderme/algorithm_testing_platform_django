"""
    #  @ModuleName: iter_files
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/9 20:59
"""
from collections import defaultdict
import os

def iter_files(rootDir, *args, **kwargs):
    """
    根据文件路径 返回文件名称 以及文件路径名称
    :param rootDir:
    :return:
    """
    filenames = defaultdict(list)
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file = os.path.join(root, file)
            if kwargs["file_type"] == "algoRunRes":
                if file.lower().endswith("jpg") or file.lower().endswith("png") or file.lower().endswith("jpeg"):
                    filenames["files"].append(file)
                elif file.lower().endswith("avi") or file.lower().endswith("mp4") or file.lower().endswith("flv"):
                    filenames["files"].append(file)
                else:
                    filenames["error_file"].append(file)
            elif kwargs["file_type"] == "algoPerssion":
                if file.lower().endswith('xml'):
                    filenames["xmls"].append(file)
                if file.lower().endswith("jpg") or file.lower().endswith("png") or file.lower().endswith("jpeg"):
                    filenames["files"].append(file)
                # 如果存在其他的类型需要时候在定义
            else:
                pass
        for dir in dirs:
            iter_files(dir)

    return filenames
