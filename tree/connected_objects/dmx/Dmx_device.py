from tree.connected_objects.Lamp import Lamp
from time import sleep

class Dmx_device(Lamp):
    """
    This is a dmx device
    """
    def __init__(self, name, relay, addr, dmx):
        Lamp.__init__(self, name, relay)
        self.dmx = dmx
        self.addr = addr

    def set(self, channel, value):
        self.dmx.set(self.addr + channel.value - 1, value)

    def connect(self):
        if not self.connected:
            while not self.dmx.connect(self.addr):
                sleep(1)
            self.connected = True

    def disconnect(self):
        if self.connected:
            self.dmx.disconnect(self.addr)
            self.connected = False

    def __str__(self):
        return str(self.addr)
