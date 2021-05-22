from tree.connected_objects.dmx.Dmx_device import Dmx_device
from enum import Enum

class Dmx_dimmable_light(Dmx_device):
    """
    Simple dimmer light in dmx
    """
    def __init__(self, name, relay, addr, dmx):
        Dmx_device.__init__(self, name, relay, addr, dmx)
        self.dimmer = 0

    def set_dimmer(self, value):
        if self.dimmer != value:
            super().set(CHANNEL.dimmer, value)
        self.dimmer = value

    def connect(self):
        if self.dimmer == 0:
            super().set_state(True)
        super().connect()

    def disconnect(self):
        if self.dimmer == 0:
            super().set_state(False)
        super().disconnect()

    def reload(self, other):
        if isinstance(other, Dmx_dimmable_light):
            super().reload(other)
            self.dimmer = other.dimmer

    def __eq__(self, other):
        if isinstance(other, Dmx_dimmable_light):
            return super().__eq__(other)\
                    and self.dimmer == other.dimmer
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Dmx_dimmable_light\n")
        string += f"- dimmer : {self.dimmer}"
        return string



class CHANNEL(Enum):
    dimmer = 1

