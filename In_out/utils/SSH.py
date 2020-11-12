import paramiko

class SSH:
    """
    Permet de se connecté au SSH d'un host distant
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        self.ssh.connect(hostname=self.host, username=self.user, password=self.password, port=22)

    def command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command("cmd.exe /c "+command)
        return str(stdout.read())

    def deconnect(self):
        self.ssh.close()

