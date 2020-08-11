from serial import Serial
from enum import Enum

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
        self.port = Serial(addr, baudrate=9600)

    def send(self, zone, action, value):
        self.port.write(("<1" + str(zone) + action.value + (value < 10)*"0" +  str(value) + "\r").encode('ascii') + bytes(0x0d))

    def get_all_infos(self, zone):
        self.port.write(("?1" + str(zone) + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline().split("<")[1]
        print(output)

        return [int(output[i:i+1]) for i in range(output-1)]

    def get_info(self, zone, action):
        self.port.write(("?1" + str(zone) + action.value + "\r").encode("ascii") + bytes(0x0d))
        self.port.readline() # useless
        output = self.port.readline().split("<")[1]
        print(output)

        return output


