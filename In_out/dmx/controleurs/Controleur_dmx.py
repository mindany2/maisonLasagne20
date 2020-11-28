from In_out.utils.DMX import DMX
from threading import Lock
from utils.Logger import Logger
from time import sleep

class Controleur_dmx:
    """
    Le controleur dmx
    """
    mutex = Lock()

    def __init__(self, transmetter = None):
        self.transmetter = transmetter

    def set(self, channel, value):
        if self.transmetter:
            self.transmetter.test(channel)

