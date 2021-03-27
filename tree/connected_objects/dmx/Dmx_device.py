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
        if self.connected:
            self.dmx.connect(self.addr)
            print(f"{self.name} is connected")

    def disconnect(self):
        if self.connected:
            self.dmx.disconnect(self.addr)
            print(f"{self.name} is disconnected")
        super().disconnect()

    def __str__(self):
        return str(self.addr)
