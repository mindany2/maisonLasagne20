from serial import Serial
from enum import Enum
from threading import Lock

class ACTION(Enum):
    power = "PR"
    mute = "MU"
    distrub = "DT"
    volume = "VO"
    trebe = "TR"
    bass = "BS"
    balance = "BL"
    source = "CH"

class DAX66:
    """
    Backend ampli 6 zones bar
    """

    def __init__(self, addr):
        self.port = Serial(addr, baudrate=9600, timeout = 0.1)
        self.mutex = Lock()
        self.etat = False

    def send(self, zone, action, value):
        if not(self.etat):
            return
        self.mutex.acquire()
        self.port.write(("<1" + str(zone) + action.value + (value < 10)*"0" +  str(value) + "\r").encode('ascii') + bytes(0x0d))

        self.port.readline() # useless
        self.mutex.release()

    def get_all_infos(self, zone):
        if not(self.etat):
            return None
        self.mutex.acquire()
        self.port.write(("?1" + str(zone) + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline()
        print(output)
        output = str(output).split(">")[1].replace("\\r","").replace("\\n","")
        self.mutex.release()

        return [int(output[2*i:2*(i+1)]) for i in range(int(len(output)/2))]

    def get_info(self, zone, action):
        if not(self.etat):
            return None
        self.mutex.acquire()
        self.port.write(("?1" + str(zone) + action.value + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline().split("<")[1]
        print(output)
        self.mutex.release()

        return output


