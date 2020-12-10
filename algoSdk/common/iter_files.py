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
            if kwargs["file_type"] == "algoRunRes":
                file = os.path.join(root, file)
                if file.lower().endswith("jpg") or file.lower().endswith("png") or file.lower().endswith("jpeg"):
                    filenames["image_dir"].append(file)
                elif file.lower().endswith("avi") or file.lower().endswith("mp4") or file.lower().endswith("flv"):
                    filenames["video_dir"].append(file)
                else:
                    filenames["error_file"].append(file)
            else:
                pass
        for dir in dirs:
            iter_files(dir)

    return filenames
