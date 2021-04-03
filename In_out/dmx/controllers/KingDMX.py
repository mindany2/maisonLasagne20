from In_out.utils.DMX import DMX
from In_out.dmx.controllers.Dmx_controller import Dmx_controller
from tree.utils.Logger import Logger
from threading import Lock

class KingDMX(Dmx_controller):
    """
    Le controler dmx kingDMX
    (can also works for different brand)
    """
    def __init__(self, addr, transmitter = []):
        Dmx_controller.__init__(self, transmitter)
        self.addr = addr
        self.dmx = DMX(addr, auto_submit=True)
        self.dmx.clear_channels()

    def set(self, channel, value):
        super().set(channel, value)
        if self.dmx:
            self.dmx.set_channel(channel, int(value))
            Logger.debug(f"send {channel} {value}")
