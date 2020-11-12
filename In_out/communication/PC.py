import os
from time import sleep
from In_out.utils.SSH import SSH
from In_out.communication.Connection import Connection
from utils.Logger import Logger
from enum import Enum

class ACTIONS(Enum):
    allumer = 0
    eteindre = 1
    key = 2
    mouse = 3

class PC(Connection):
    """
    PC distant
    """
    
    def __init__(self, nom, addr_mac, addr_ip, user, password):
        Connection.__init__(self, nom, addr_ip)
        self.addr_mac = addr_mac
        self.addr_ip = addr_ip
        self.user = user
        self.ssh = SSH(addr_ip, user, password)

    def start(self):
        Logger.info("On allume le PC "+self.nom)
        os.system("sudo etherwake -i eth0 "+self.addr_mac)

    def etat(self):
        return os.system("ping -c 1 " + self.addr_ip) == 0

    def connect(self):
        # on l'allume s'il était eteint
        self.lock()
        if not(self.etat()):
            self.start()
            sleep(30)

        # on start le serveur python sur le PC distant
        Logger.debug("connection ssh à "+self.nom)
        self.ssh.connect()
        self.ssh.command("cd C:\\Users\\{}\\Documents\\Leo\\maison".format(self.user))
        self.ssh.command("python Main_PC_control.py")
        self.unlock()

    def deconnect(self):
        self.lock()
        self.check_for_deconnection()
        self.ssh.command("shutdown -s -t 0")
        self.ssh.deconnect()
        self.unlock()







