from tree.connected_objects.Connected_object import Connected_object
from time import sleep
from threading import Lock
from In_out.external_boards.relay.Relay import STATE
from tree.utils.Logger import Logger

class Lamp(Connected_object):
    """
    A simple ON/OFF lamp 
    """
    def __init__(self, name, relay, invert = False):
        Connected_object.__init__(self, name)
        self.relay =  relay
        self.invert = invert
        self.force = False
        self.connected = False

    def set(self, on_off):
        self.set_relay(on_off)

    def connect(self):
        if not(self.connected):
            if not(self.force):
                self.set_relay(True)
            self.connected = True

    def disconnect(self):
        if self.connected:
            if not(self.force):
                self.set_relay(False)
            self.connected = False

    def force_relay(self, force):
        # force the relay always to ON
        self.force = force
        if force:
            self.set_relay(STATE.ON)
        elif not(self.connected):
            self.set_relay(STATE.OFF)

    def set_relay(self, on_off):
        if self.invert:
            on_off = not(on_off)

        if on_off:
            state = STATE.ON
        else:
            state = STATE.OFF
        if self.relay.state != state:
            self.relay.set(state)

    def state(self):
        return self.relay.state

    def reload(self, other):
        if isinstance(other, Lamp):
            self.force == other.force

    def __eq__(self, other):
        if isinstance(other, Lamp):
            return super().__eq__(other)\
                    and self.relay == other.relay\
                    and self.force == other.force\
                    and self.invert == other.invert
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : lamp\n")
        string += "".join("- Relay : {}\n".format(self.relay))
        return string

