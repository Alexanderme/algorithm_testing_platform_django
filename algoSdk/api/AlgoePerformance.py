"""
    #  @ModuleName: AlgoePerformance
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/21 20:07
"""
# import logging
#
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from ..common.connect_server import ParamikoCentos
# from ..serializers.serializers import AlgoResourceOccupationSerializer
#
# logger = logging.getLogger(__name__)
#
# class AlgoResourceOccupation(APIView):
#     """
#     用于验证算法占用服务器资源信息
#     :return:
#     """
#     def post(self, requests, *args, **kwargs):
#         data = requests.data
#         obj = AlgoResourceOccupationSerializer(data=data)
#         if not obj.is_valid():
#             logging.exception(obj)
#             return Response({"87": "参数错误"})
#         file_name = requests.files.get('file_name')
#         image_name = obj.data.get('image_name')
#         server_ip = obj.data.get('server_ip')
#         server_port = int(obj.data.get('server_port'))
#         server_user = obj.data.get('server_user')
#         server_passwd = obj.data.get('server_passwd')
#
#         server = ParamikoCentos(hostname=server_ip, username=server_user, password=server_passwd, port=server_port)
#         try:
#             server.type_login_root()
#         except Exception as e:
#             logging.exception(e)
#             return Response({"code": 94, "msg": "连接服务器失败"})
#
#         connect_server_remote_dir = ""
#
#         server.sftp_put_dir(files_dir, remote_dir)
#         server.sftp_put_dir('extremevision/libs/shell', remote_dir)
#
#         # 获取到容器id
#         contain_id = server.exec_command(run_sdk_config_GPU + f"{image_name}")[:8]
#         # 执行授权文件, 并且运行算法
#         server.exec_command(f"docker exec  {contain_id} bash /tmp/sdk_resource_occupation.sh")
#         server.exec_command(f"docker exec  -t  {contain_id} python3 /tmp/get_remote_use.py {filename}")
#
#         res = server.exec_command(f"cat /tmp/ljx/res_used.txt")
#         print(res)
#         server.exec_command(f"docker stop  {contain_id}")
#         return jsonify(errno=RET.OK, errmsg=res)
#


