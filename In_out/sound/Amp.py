from In_out.sound.Channel import Channel
from In_out.external_boards.relay.Relay import STATE
from tree.utils.Logger import Logger
from time import sleep
from threading import Lock

class Amp:
    """
    A amp with somes channels
    """

    def __init__(self, name, relay, output, nb_channels = 6):
        self.relay = relay
        self.name = name
        self.mutex = Lock()
        self.channels = [Channel(i, output) for i in range(1,nb_channels+1)]

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def state(self):
        return self.relay.state == STATE.ON

    def get_channel(self, i):
        try:
            return self.channels[i-1]
        except:
            Logger.error("")
            return None

    def set_state(self, state):
        if self.state() != state:
            if state:
                self.power_on()
            else:
                self.power_off()
            
    def power_on(self):
        self.mutex.acquire()
        if not(self.state()):
            self.relay.set(STATE.ON)
            sleep(1)
            conn = self.connect()
            if not(conn):
                self.relay.set(STATE.OFF)
        self.mutex.release()
        return self.state()

    def connect(self):
        # connect to the amp
        return False

    def disconnect(self):
        # disconnect the amp
        pass

    def power_off(self):
        self.mutex.acquire()
        if self.state():
            # check if all the channels are off
            test = True
            for channel in self.channels:
                if channel.power:
                    test = False
            if test:
                self.disconnect()
                self.relay.set(STATE.OFF)
        self.mutex.release()
