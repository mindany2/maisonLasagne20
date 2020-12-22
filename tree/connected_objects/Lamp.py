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
        self.state = STATE.OFF

    def connect(self):
        if not(self.connected):
            if not(self.force):
                self.set_state(True)
            self.connected = True

    def disconnect(self):
        if self.connected:
            if not(self.force):
                self.set_state(False)
            self.connected = False

    def force_relay(self, force):
        # force the relay always to ON
        if self.force != force:
            self.force = force
            if force:
                self.relay.set(STATE.ON)
            elif not(self.connected):
                self.relay.set(STATE.OFF)

    def set_state(self, on_off):
        if self.force:
            return 
        if self.invert:
            on_off = not(on_off)

        state = [STATE.OFF, STATE.ON][bool(on_off)]
        if state != self.state:
            self.relay.set(state)
            self.state = state

    def reload(self, other):
        if isinstance(other, Lamp):
            self.force = other.force
            self.state = other.state

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

