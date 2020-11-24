import os
from time import sleep
from In_out.communication.Connection import Connection
from utils.communication.control.Cmd import Cmd
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
        # le serveur python devrait être lancé automatiquement au démarrage
        self.unlock()

    def deconnect(self):
        self.lock()
        print("check_for_deconnection")
        self.check_for_deconnection()
        print("shutdown")
        self.send(Cmd("shutdown -s -t 0"))
        print("deconnect")
        self.deconnect()
        self.unlock()







