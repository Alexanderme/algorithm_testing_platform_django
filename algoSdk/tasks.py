"""
    #  @ModuleName: task
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/9 20:32
"""

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from time import sleep
from celery import shared_task

class TestView3(GenericAPIView):

  @classmethod
  @shared_task
  def sleep(self, duration):
    sleep(duration)
    return Response("成功", status=200)
