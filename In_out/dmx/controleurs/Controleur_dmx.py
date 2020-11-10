from In_out.utils.DMX import DMX
from threading import Lock
from utils.Logger import Logger

class Controleur_dmx:
    """
    Le controleur dmx kingDMX
    """
    mutex = Lock()

    def __init__(self, addr):
        self.addr = addr

    def set(self, channel, value):
        pass

