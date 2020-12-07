"""
    #  @ModuleName: urls
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/4 14:34
"""
from django.conf.urls import url

from .api.IasBuild import IasPackage


urlpatterns = [
    url(r'sdk_authorization/iasPackage', IasPackage.as_view()),
]
