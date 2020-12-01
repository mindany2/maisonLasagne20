import os
from time import sleep
from In_out.network.Connection import Connection
from In_out.network.communication.control.Cmd import Cmd
from enum import Enum
from threading import Thread

class ACTIONS(Enum):
    power_on = 0
    power_off = 1
    key = 2
    mouse = 3

class PC(Connection):
    """
    A distant PC with the python serveur running on it at the startup :
    Launch Main_PC_control.py
    """
    
    def __init__(self, name, addr_mac, addr_ip, user, password):
        Connection.__init__(self, name, addr_ip)
        self.addr_mac = addr_mac
        self.addr_ip = addr_ip

    def power_on(self):
        os.system("sudo etherwake -i eth0 "+self.addr_mac)

    def state(self):
        return os.system("ping -c 1 " + self.addr_ip) == 0

    def connect(self):
        self.lock()
        # start the pc if it is down
        if not(self.state()):
            self.power_on()
            sleep(75) # time to the pc to startup
        # now the serveur should be launch
        self.unlock()

    def disconnect(self):
        self.lock()
        self.check_for_disconnection()
        self.send(Cmd("shutdown -s -t 0"))
        self.disconnect()
        self.unlock()







