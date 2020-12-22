"""
    #  @ModuleName: connect_server
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/12/21 20:08
"""

import paramiko
import stat
import os
import traceback


class ParamikoCentos:
    """
    用于连接服务器, 远程处理算法问题
    """

    def __init__(self, hostname, port=22, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.t = paramiko.Transport((self.hostname, self.port))
        self.ssh = paramiko.SSHClient()

    # 登录要测试的主机（linux主机）
    def type_login_root(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, self.port, self.username, self.password)
        self.t.connect(username=self.username, password=self.password)

    # 执行linux命令
    def exec_command(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        results_err = stderr.read().decode('utf-8')
        results_rig = stdout.read().decode('utf-8')
        if results_err != '':
            print('--------------------------results_err',results_err)
            return False
        else:
            return results_rig

    # 批量顺序执行
    def exec_commands(self, cmd_list=[]):
        CmdDict = {}
        for c in cmd_list:
            CmdMes = self.exec_command(c)
            CmdDict[c] = CmdMes
        return CmdDict

    # 断开连接
    def shutdown_root(self):
        self.ssh.close()
        self.t.close()

    # 从远程服务器获取文件到本地
    def sftp_get(self, remotefile, localfile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.get(remotefile, localfile)

    # 从本地上传文件到远程服务器
    def sftp_put(self, localfile, remotefile):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.t)
            sftp.put(localfile, remotefile)
            return True
        except Exception as e:
            print(e)
            return False

    def _get_all_files_in_local_dir(self, local_dir):
        all_files = list()

        for root, dirs, files in os.walk(local_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                all_files.append(filename)

        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.t)

            if remote_dir[-1] == "/":
                remote_dir = remote_dir[0:-1]

            all_files = self._get_all_files_in_local_dir(local_dir)
            for file in all_files:
                file = file.replace("\\", "/")
                remote_filename = file.replace(local_dir, remote_dir).replace("\\", "/")
                remote_path = os.path.dirname(remote_filename)


                try:
                    sftp.stat(remote_path)
                except:
                    self.exec_command('mkdir -p %s' % remote_path)  # 使用这个远程执行命令
                sftp.put(file, remote_filename)
        except:
            print('ssh get dir from master failed.')
            print(traceback.format_exc())

