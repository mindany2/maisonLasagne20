from tree.connected_objects.Lamp import Lamp
import time

class Dmx_device(Lamp):
    """
    This is a dmx device
    """
    def __init__(self, name, relay, addr, dmx):
        Lamp.__init__(self, name, relay)
        self.dmx = dmx
        self.addr = addr

    def set(self, channel, value):
        assert self.connected, "Need to connect the device before"
        self.dmx.set(self.addr + channel.value - 1, value)

    def connect(self):
        if not self.connected:
            while not self.dmx.connect(self.addr):
                time.sleep(1)
            self.connected = True
            return True

    def disconnect(self):
        if self.connected:
            self.dmx.disconnect(self.addr)
            self.connected = False

    def __eq__(self, other):
        if isinstance(other, Dmx_device):
            return super().__eq__(other)\
                    and self.dmx == other.dmx\
                    and self.addr == other.addr
        return False

    def __str__(self):
        string = super().__str__()
        string += f"- Address : {self.addr}\n"
        string += f"- Dmx : {self.dmx}\n"
        return string
