from In_out.utils.DAX66 import DAX66
from In_out.sound.Amp import Amp
from tree.utils.Logger import Logger
from time import sleep
from threading import Lock

class Amp_6_channels(Amp):
    """
    Manage the DAX66 amplifier
    https://tinyurl.com/dax66amp
    """

    def __init__(self, name, relay, addr):
        self.bus = DAX66(addr)
        Amp.__init__(self, name, relay, self.bus, nb_channels = 6)

    def connect(self):
        # time for the amp to setup the speakers
        sleep(2)
        return self.bus.connect()

    def disconnect(self):
        self.bus.disconnect()
