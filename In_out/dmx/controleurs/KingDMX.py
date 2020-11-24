from In_out.utils.DMX import DMX
from In_out.dmx.controleurs.Controleur_dmx import Controleur_dmx
from threading import Lock
from utils.Logger import Logger

class KingDMX(Controleur_dmx):
    """
    Le controleur dmx kingDMX
    """
    def __init__(self, addr, transmetter):
        Controleur_dmx.__init__(self, transmetter)
        self.addr = addr
        self.dmx = DMX(addr, auto_submit=True)
        self.dmx.clear_channels()

    def set(self, channel, value):
        super().set(channel, value)
        if self.dmx:
            self.dmx.set_channel(channel, int(value))
