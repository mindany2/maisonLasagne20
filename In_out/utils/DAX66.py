from enum import Enum
from time import sleep
from tree.utils.Logger import Logger
from threading import Lock
try:
    from serial import Serial
except:
    pass

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
    Backend amp 6 channels
    """

    def __init__(self, addr):
        self.addr = addr
        self.mutex = Lock()
        self.port = None

    def connect(self):
        if not(self.port):
            self.mutex.acquire()
            try:
                self.port = Serial(self.addr, baudrate=9600, timeout = 0.1)
            except:
                Logger.error("Fail to connect to the amp")
                return False
            self.mutex.release()
            return True


    def disconnect(self):
        self.port = None

    def send(self, zone, action, value):
        if not(self.port):
            return
        self.mutex.acquire()
        self.port.write(("<1" + str(zone) + action.value + (value < 10)*"0" +  str(value) + "\r").encode('ascii') + bytes(0x0d))

        self.port.readline()# useless
        sleep(0.1)
        self.mutex.release()

    def get_all_infos(self, zone):
        if not(self.port):
            return None
        self.mutex.acquire()
        self.port.write(("?1" + str(zone) + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline()
        try:
            output = str(output).split(">")[1].replace("\\r","").replace("\\n","").replace("'","")
        except:
            self.mutex.release()
            return [0 for i in range(11)]
        sleep(0.1)
        self.mutex.release()

        return [int(output[2*i:2*(i+1)]) for i in range(int(len(output)/2))]

    def get_info(self, zone, action):
        if not(self.port):
            return None
        self.mutex.acquire()
        self.port.write(("?1" + str(zone) + action.value + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline()
        sleep(0.1)
        self.mutex.release()

        return int(output[-4:-2])


