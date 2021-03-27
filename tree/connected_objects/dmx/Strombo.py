from tree.connected_objects.dmx.Dmx_device import Dmx_device
from enum import Enum

class Strombo(Dmx_device):
    """
    Small stromboscop : Fun Generation LED Pot Strobe 100
    https://www.thomann.de/intl/fun_generation_led_pot_strobe_100.htm
    """

    def __init__(self, name, relay, addr, dmx):
        Dmx_device.__init__(self, name, relay, addr, dmx)
        self.dimmer = 0
        self.strombo = 0

    def set_dimmer(self, value):
        if self.dimmer != value:
            super().set(CHANNEL.dimmer, value)
        self.dimmer = value

    def set_strombo(self, value):
        if self.strombo != value:
            super().set(CHANNEL.strombo, value)
        self.strombo = value

    def lock_dimmer(self):
        super().lock()

    def unlock_dimmer(self):
        super().unlock()

    def reload(self, other):
        if isinstance(other, Strombo):
            self.dimmer == other.dimmer
            self.strombo == other.strombo

    def __eq__(self, other):
        if isinstance(other, Strombo):
            return super().__eq__(other)\
                    and super() == other.dmx\
                    and self.dimmer == other.dimmer\
                    and self.strombo == other.strombo
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Strombo\n")
        string += "".join("- Dmx : {}\n".format(super()))
        return string



class CHANNEL(Enum):
    dimmer = 1
    program = 2
    strombo = 3

