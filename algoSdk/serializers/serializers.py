"""
    #  @ModuleName: serializers
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/3 16:46
"""
from rest_framework import serializers


class IasPackageSerializers(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)
    port = serializers.IntegerField(min_value=10000, max_value=60000)
    version = serializers.CharField(max_length=12, default='4.1')

class VasPackageSerializers(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)
    port = serializers.IntegerField(min_value=10000, max_value=60000)
    version = serializers.CharField(max_length=12, default='4.1')