from time import time, sleep
from In_out.external_boards.relay.Relay import STATE
from threading import Thread

TIME_OUT = 3
CONNECTION_TIME = 2

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
            if not(self.state()):
                self.relay.set(STATE.ON)
                sleep(CONNECTION_TIME) # tps de connection
                thread = Thread(target = self.check_for_deconnection)
                thread.name = "Wireless_transmitter check_for_deconnection"
                thread.start()

    def check_for_deconnection(self):
        while time()-self.tps < TIME_OUT:
            sleep(1)
        self.relay.set(STATE.OFF)
  
    def __str__(self):
        return "Relay : {} in range ({},{})".format(self.relay, self.addr_min, self.addr_max)  

       
