from In_out.utils.DAX66 import DAX66
from In_out.sound.Amp import Amp
from tree.utils.Logger import Logger
from time import sleep
from threading import Lock

class Ampli_6_channels(Amp):
    """
    Manage the DAX66 amplifier
    https://tinyurl.com/dax66amp
    """

    def init(self, addr, relay):
        self.bus = DAX66(addr)
        Amp.__init__(self, relay, self.bus, nb_channels = 6)
        for channel in self.channels:
            channel.set_bus(self.bus)
