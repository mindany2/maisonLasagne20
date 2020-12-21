
class Dmx_device:
    """
    Store the address of a dmx device
    """
    def __init__(self, dmx, addr):
        self.dmx = dmx
        self.addr = addr

    def set(self, channel, value):
        self.dmx.set(self.addr + channel.value - 1, value)

    def __str__(self):
        return self.addr
