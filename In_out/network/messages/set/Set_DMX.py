from In_out.network.messages.Message import Message
from enum import Enum

class Set_DMX(Message):

    def __init__(self, addr, value):
        # if value = -1 : connect, value = -2 : disconnect
        self.addr = addr
        self.value = value

    def do(self, getter):
        dmx = getter.get_manager().get_dmx()
        if self.value == -1:
            dmx.connect(self.addr)
        elif self.value == -2:
            dmx.disconnect(self.addr)
        else:
            dmx.set(self.addr, self.value)
        

    def __str__(self):
        return f"Set_DMX : addr={self.addr}, value={self.value}"
