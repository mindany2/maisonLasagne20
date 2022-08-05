from time import time, sleep
from In_out.external_boards.relay.Relay import STATE
from tree.utils.Logger import Logger

TIME_OUT = 3
CONNECTION_TIME = 5

class Wireless_transmitter:
    """
    Manage the relay of a wireless dmx transmitter
    """
    def __init__(self, relay, addr_min, addr_max):
        self.relay = relay
        self.addr_min = addr_min
        self.addr_max = addr_max
        self.tps = time()

    def state(self):
        return self.relay.state == STATE.ON

    def test(self, addr):
        if self.addr_min <= addr and addr <= self.addr_max:
            self.tps = time()
            return True
        return False

    def power_on(self):
        if not(self.state()):
            Logger.debug(f"power on {self.relay}")
            self.relay.set(STATE.ON)
            sleep(CONNECTION_TIME)

    def power_off(self):
        if self.state():
            Logger.debug(f"power off {self.relay}")
            self.relay.set(STATE.OFF)
  
    def __str__(self):
        return "Relay : {} in range ({},{})".format(self.relay, self.addr_min, self.addr_max)  

       
