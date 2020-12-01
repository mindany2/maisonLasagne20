from In_out.utils.DMX import DMX
from threading import Lock
from time import sleep

class Dmx_controller:
    """
    A dmx output
    """

    def __init__(self, transmitter = None):
        self.transmitter = transmitter
        self.mutex = Lock()

    def set(self, channel, value):
        if self.transmitter:
            self.transmitter.test(channel)

