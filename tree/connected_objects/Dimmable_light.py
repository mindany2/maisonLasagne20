from tree.connected_objects.Connected_object import Connected_object
from In_out.external_boards.relay.Relay import STATE
from In_out.external_boards.Triak import STATE_TRIAK
from enum import Enum
from time import sleep

class BULD(Enum):
    """
    Each dimmable light have is own range of dimmer
    buld is define by the last number of the serial number of the buld
    """
    # type  = (maxi,mini)
    buld_63 = (400,80)
    buld_65 = (400,160)
    buld_91 = (430,50)
    buld_64 = (430,180)
    buld_73 = (400,130)
    buld_61 = (430,250)
    buld_200 = (370,130)


class Dimmable_light(Connected_object):
    """
    A dimmable light control by a triak
    """
    def __init__(self, name, triak, type_buld):
        Connected_object.__init__(self, name)
        self.triak = triak
        self.type_buld = type_buld
        self.dimmer = 0
        # power off the light
        self.triak.set(10**9,STATE_TRIAK.off)

    def connect(self):
        # setup dimmer if it is necessary
        if self.dimmer == 0:
            self.triak.set(self.convert(0))
        elif self.dimmer == 100:
            self.triak.set(self.convert(100))

    def disconnect(self):
        #disconnect if it is necessary
        if self.dimmer == 0:
            # setup dimmer
            self.triak.set(10**9, STATE_TRIAK.off)
        elif self.dimmer == 100:
            # remove dimmer
            self.triak.set(10**9, STATE_TRIAK.on)

    def set_dimmer(self, dimmer):
        value = self.convert(dimmer)
        self.triak.set(value)
        self.dimmer = int(dimmer)

    def lock_dimmer(self):
        self.lock()

    def test_dimmer(self):
        return self.test()

    def unlock_dimmer(self):
        self.unlock()

    def convert(self, dimmer):
        # convert dimmer value to triak value
        maxi, mini = self.type_buld.value
        value = int(mini + (maxi-mini)*(1-dimmer/100))
        return value

    def reload(self, other):
        if isinstance(other, Dimmable_light):
            self.dimmer == other.dimmer

    def __eq__(self, other):
        if isinstance(other, Dimmable_light):
            return super().__eq__(other)\
                    and self.triak == other.triak\
                    and self.dimmer == other.dimmer\
                    and self.type_buld == other.type_buld
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : dimmable_light\n")
        string += "".join("- Triak : {}\n".format(self.triak))
        string += "".join("- Buld : {}\n".format(self.type_buld))
        return string

