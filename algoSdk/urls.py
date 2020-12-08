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


urlpatterns = [
    url(r'sdk/iasPackage', IasPackage.as_view()),
    url(r'sdk/vasPackage', VasPackage.as_view()),
    url(r'sdk/algoMessage', AlgoOpencvVersion.as_view()),
]
