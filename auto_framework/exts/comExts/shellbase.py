import paramiko

from exts.utils import str_to_list


class SSH():

    def __init__(self,ip,username,password,port=22):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def shell_cmd(self,cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, self.username, self.password,timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            content = stdout.read().decode('utf-8')
            res = content.split('\n')
            ssh.close()
            return res
        except Exception as e:
            print('远程执行shell命令失败！！！')
            return False

    def shell_upload(self,localpath,remotepath):
        try:
            transport = paramiko.Transport((self.ip,self.port))
            transport.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(localpath, remotepath)
            transport.close()
            print('文件上传成功，上传路径：{}'.format(remotepath))
            return True
        except Exception as e:
            print('文件上传失败！！！')
            return False

    def shell_download(self,localpath,remotepath):
        try:
            transport = paramiko.Transport((self.ip,self.port))
            transport.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remotepath,localpath)
            transport.close()
            print('文件下载成功，下载路径：{}'.format(localpath))
            return True
        except Exception as e:
            print('文件下载失败！！！')
            return False


if __name__ == '__main__':
    ip = '172.168.13.232'
    username = 'root'
    password = '111111111111111a!'
    cmd = 'date'
    ssh = SSH(ip,username,password)
    res = ssh.shell_cmd(cmd)
    print(res)