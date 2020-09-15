from In_out.utils.DMX import DMX
from threading import Lock
from utils.Logger import Logger

class Controleur_dmx:
    """
    Le controleur dmx kingDMX
    """
    dmx = None
    mutex = Lock()

    @classmethod
    def init(self, addr):
        self.dmx = DMX(addr, auto_submit=True)
        self.addr = addr
        self.dmx.clear_channels()

    @classmethod
    def set(self, channel, value):
        self.mutex.acquire()
        if self.dmx:
            self.dmx.set_channel(channel, value)
        self.mutex.release()

