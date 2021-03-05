from tree.connected_objects.Lamp import Lamp
from time import sleep
from enum import Enum

class Dmx_dimmable_light(Lamp):
    """
    Simple dimmer light in dmx
    """
    def __init__(self, name, relay, controler):
        Lamp.__init__(self, name, relay)
        self.dmx = controler
        self.dimmer = 0

    def set_dimmer(self, value):
        if self.dimmer != value:
            self.dmx.set(CHANNEL.dimmer, value)
        self.dimmer = value

    def connect(self):
        if self.dimmer == 0:
            super().set_state(True)
            # need to wait before the light is initialise
            sleep(4)

    def disconnect(self):
        if self.dimmer == 0:
            super().set_state(False)

    def lock_dimmer(self):
        super().lock()
        if self.dimmer == 0:
            self.set_state(1)

    def test_dimmer(self):
        return super().test()

    def unlock_dimmer(self):
        super().unlock()
        if self.dimmer == 0:
            self.set_state(0)

    def reload(self, other):
        if isinstance(other, Dmx_dimmable_light):
            self.dimmer == other.dimmer

    def __eq__(self, other):
        if isinstance(other, Dmx_dimmable_light):
            return super().__eq__(other)\
                    and self.dmx == other.dmx\
                    and self.dimmer == other.dimmer
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Dmx_dimmable_light\n")
        string += "".join("- Dmx : {}\n".format(self.dmx))
        return string



class CHANNEL(Enum):
    dimmer = 1

