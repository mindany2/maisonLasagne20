from tree.connected_objects.Lamp import Lamp

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
        super().connect()
        self.dmx.connect(self.addr)

    def disconnect(self):
        super().disconnect()
        self.dmx.disconnect(self.addr)

    def __str__(self):
        return str(self.addr)
