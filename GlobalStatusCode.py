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


def parameter_wrong():
    return '87', '参数错误'


def parameter_not_exist():
    return '89', '无数据'


def parameter_is_exist():
    return '88', '数据已存在'


def dockerfile_error():
    return '91', 'dockerfile生成失败'


def docker_run_faild():
    return '92', '算法启动失败'
