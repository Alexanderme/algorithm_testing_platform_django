"""
    #  @ModuleName: test.py
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/9 20:33
"""
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from ..tasks import TestView3

class TestView1(GenericAPIView):
  def get(self, request):
    TestView3.sleep(10)
    return Response("celery实验成功")