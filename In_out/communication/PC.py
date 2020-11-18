import os
from time import sleep
from In_out.utils.SSH import SSH
from In_out.communication.Connection import Connection
from utils.Logger import Logger
from enum import Enum
from threading import Thread

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
            sleep(75)

        # on start le serveur python sur le PC distant
        Logger.debug("connection ssh à "+self.nom)
        self.ssh.connect()
        """
        Thread(target=self.start_serveur).start()
        """
        self.unlock()


    def start_serveur(self):
        self.ssh.command("C:\\Users\\{}\\Documents\\Leo\\maison\\Main_PC_control.py".format(self.user))

    def deconnect(self):
        self.lock()
        print("check_for_deconnection")
        self.check_for_deconnection()
        print("shutdown")
        self.ssh.command("shutdown -s -t 0")
        print("deconnect")
        self.ssh.deconnect()
        self.unlock()







