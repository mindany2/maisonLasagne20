from In_out.utils.DMX import DMX
from threading import Lock
from time import sleep

class Dmx_controller:
    """
    A dmx output
    """

    def __init__(self, transmitters = []):
        self.transmitters = transmitters
        self.mutex = Lock()

    def set(self, channel, value):
        for transmit in self.transmitters:
            transmit.test(channel)

