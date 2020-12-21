"""
    #  @ModuleName: urls
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:34
"""
from django.conf.urls import url

from .api.IasBuild import IasPackage
from .api.VasBuild import VasPackage
from .api.AlgoMessage import AlgoOpencvVersion
from .api.AlgoRunRes import AlgoRes
from .api.CeleryTask import TaskStatus, CleanEvn, FilesResult
from .api.AlgoPerssion import GetFilesResult


urlpatterns = [
    url(r'sdk/iasPackage', IasPackage.as_view()),
    url(r'sdk/vasPackage', VasPackage.as_view()),
    url(r'sdk/algoMessage', AlgoOpencvVersion.as_view()),
    url(r'sdk/algoRes', AlgoRes.as_view()),
    url(r'sdk/taskInfo', TaskStatus.as_view()),
    url(r'sdk/fileResult', FilesResult.as_view()),
    url(r'sdk/cleanEnv', CleanEvn.as_view()),
    url(r'sdk/algoPerssion', GetFilesResult.as_view()),
]
