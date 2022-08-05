from In_out.utils.DMX import DMX
from threading import Lock
from time import sleep

class Dmx_controller:
    """
    A dmx output
    """

    def __init__(self, transmitters = []):
        self.transmitters = transmitters
        self.current_wireless = None # only one wireless at the time
        self.mutex = Lock()
        self.active_transmitter = None
        self.nb_connection = 0

    def connect(self, channel):
        self.mutex.acquire()
        for transmit in self.transmitters:
            if transmit.test(channel):
                if transmit != self.active_transmitter:
                    if self.active_transmitter: # != None
                        print(f"Bloc with {channel}")
                        self.mutex.release()
                        return False
                    print(f"OK for {channel}")
                    self.active_transmitter = transmit
                    transmit.power_on()
                self.nb_connection += 1
        self.mutex.release()
        return True

    def disconnect(self, channel):
        if self.active_transmitter and self.active_transmitter.test(channel):
            self.nb_connection -= 1
            if self.nb_connection == 0:
                self.active_transmitter.power_off()
                self.active_transmitter = None

    def set(self, channel, value):
        pass

    def __str__(self):
        return "".join([str(trans) for trans in self.transmitters])
