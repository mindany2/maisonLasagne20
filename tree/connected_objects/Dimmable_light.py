from tree.connected_objects.Connected_object import Connected_object
from In_out.external_boards.relay.Relay import STATE
from In_out.external_boards.Triak import STATE_TRIAK
from enum import Enum
from time import sleep

class BULD(Enum):
    """
    Each dimmable light have is own range of dimmer
    type is define by the last number of the serial number of the buld
    """
    # type  = (maxi,mini)
    type_63 = (400,80)
    type_65 = (400,160)
    type_91 = (430,50)
    type_64 = (430,180)
    type_73 = (400,130)
    type_61 = (430,250)
    type_200 = (370,130)


class Dimmable_light(Connected_object):
    """
    A dimmable light control by a triac
    """
    def __init__(self, name, triac, type_buld):
        Connected_object.__init__(self, name)
        self.triac = triac
        self.type_buld = type_buld
        self.dimmer = 0
        # power off the light
        self.triac.set(10**9,STATE_TRIAK.off)

    def connect(self):
        # setup dimmer if it is necessary
        if self.dimmer == 0:
            self.triac.set(self.convert(0))
        elif self.dimmer == 100:
            self.triac.set(self.convert(100))

    def disconnect(self):
        #disconnect if it is necessary
        if self.dimmer == 0:
            # setup dimmer
            self.triac.set(10**9, STATE_TRIAK.off)
        elif self.dimmer == 100:
            # remove dimmer
            self.triac.set(10**9, STATE_TRIAK.on)

    def set_dimmer(self, dimmer):
        value = self.convert(dimmer)
        self.triac.set(value)
        self.dimmer = int(dimmer)

    def lock_dimmer(self):
        self.lock()

    def test_dimmer(self):
        return self.test()

    def unlock_dimmer(self):
        self.unlock()

    def convert(self, dimmer):
        # convert dimmer value to triac value
        maxi, mini = self.type_buld.value
        value = int(mini + (maxi-mini)*(1-dimmer/100))
        return value
