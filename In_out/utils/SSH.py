import paramiko
from tree.utils.Logger import Logger

class SSH:
    """
    Allow to connect in ssh to a remote device
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        self.ssh.connect(hostname=self.host, username=self.user, password=self.password, port=22)
        Logger.info("ssh connected to "+self.host)

    def command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        Logger.info("ssh command : "+command + "\n" + str(stdout.read()))
        return str(stdout.read())

    def disconnect(self):
        self.ssh.close()
        Logger.info("ssh disconnected to "+self.host)

