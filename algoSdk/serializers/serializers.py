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


class VasPackageSerializers(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)
    port = serializers.IntegerField(min_value=10000, max_value=60000)


class AlgoOpencvVersionSerializers(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)


class AlgoResSerializer(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)
    args = serializers.CharField(max_length=1024, required=False)
    file_name = serializers.FileField()

class CeleryTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=124)

class FilesResultSerializer(serializers.Serializer):
    files = serializers.CharField(max_length=256)

class CleanEnvSerializer(serializers.Serializer):
    container_id = serializers.CharField(max_length=124, required=False)
    ori_files_dir = serializers.CharField(max_length=512, required=False)
    res_files_dir = serializers.CharField(max_length=512, required=False)


class GetFilesResultSerializer(serializers.Serializer):
    image_name = serializers.CharField(max_length=512)
    args = serializers.CharField(max_length=2014, required=False)
    tag_names = serializers.CharField(max_length=124)
    alert_info = serializers.CharField(max_length=24)
    iou = serializers.FloatField(max_value=1, min_value=0)
    file_name = serializers.FileField()