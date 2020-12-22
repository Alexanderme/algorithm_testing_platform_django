"""
    #  @ModuleName: GlobalStatusCode
    #  @Function: 用于制定标准先不使用
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:26
"""


def success():
    return '100', '成功'


def fail():
    return '99', '失败'


def mysql_error():
    return '98', '数据库查询错误'


def env_error():
    return '97', '系统环境处理相关失败'


def upload_downfile_error():
    return '96', '文件操作相关失败'


def celery_error():
    return '95', '异步任务相关失败'


def connect_server():
    return '94', '连接服务器相关失败'


def parameter_wrong():
    return '87', '参数错误'


def parameter_not_exist():
    return '89', '无数据'


def parameter_is_exist():
    return '88', '数据已存在'


def algo_error():
    return '90', '算法相关失败'
